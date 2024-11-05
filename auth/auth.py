from jwt import ExpiredSignatureError, decode as jwt_decode
from fastapi import Request, HTTPException
import base64
from hashlib import sha256
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, jwe, ExpiredSignatureError
from enum import Enum

from database.model.user.api import get_user
from database.model.user import User
from database.model.token.api import is_token_revoked
from database.init import get_db_directly
from config.config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

public_endpoints = ["/", "/signup", "/signin", "/docs", "/openapi.json"]


# Enum for User Roles
class Role(str, Enum):
    normal = "normal"
    manager = "manager"


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public endpoints
        if request.url.path in public_endpoints:
            return await call_next(request)

        try:
            # Authenticate the request and get claims from token
            claims = await self.authenticate(request)
            # Attach user data to request state after validating token and user
            await self.attach_user_to_request(request, claims)

        except ExpiredSignatureError:
            # Handle expired token error
            return self.__json_error_response(401, "Token expired")
        except HTTPException as auth_error:
            # Handle authentication-specific HTTP exceptions
            return self.__json_error_response(auth_error.status_code, auth_error.detail)
        except Exception as e:
            # Handle any other unexpected authentication errors
            return self.__json_error_response(401, "Authentication failed: " + str(e))

        # Continue with the request if authentication succeeds
        return await call_next(request)

    async def authenticate(self, request: Request) -> dict:
        """Extract, decrypt, and validate the token, returning claims if valid."""
        token = await oauth2_scheme(request)
        if not token:
            raise HTTPException(status_code=401, detail="No authentication token provided")

        decrypted_token = self.__decrypt_token(token)
        return self.__decode_jwt_claims(decrypted_token)

    async def attach_user_to_request(self, request: Request, claims: dict):
        """Check token revocation and attach user data to the request state."""
        jti = claims.get("jti")
        user_id = claims.get("user_id")
        if not jti or not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        with get_db_directly() as db:
            if is_token_revoked(db, jti):
                raise HTTPException(status_code=401, detail="Token revoked")

            user = get_user(db, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            request.state.user = user
            request.state.jti = jti

    def __decrypt_token(self, token: str) -> bytes:
        """Decrypt the provided token."""
        try:
            decrypted_token = jwe.decrypt(base64.urlsafe_b64decode(token), settings.JWE_SECRET_KEY.encode())
            if not decrypted_token:
                raise HTTPException(status_code=401, detail="Invalid token")
            return decrypted_token
        except Exception:
            raise HTTPException(status_code=401, detail="Token decryption failed")

    def __decode_jwt_claims(self, decrypted_token: bytes) -> dict:
        """Decode the JWT claims, verifying signature and expiration."""
        try:
            return jwt.decode(decrypted_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or corrupted token")

    def __json_error_response(self, status_code: int, message: str) -> JSONResponse:
        """Return a JSON response with a given error message and status code."""
        return JSONResponse(status_code=status_code, content={"message": message})


# Dependency to authenticate user and check roles
def authenticate(required_role: Role | None = None):
    def role_checker(request: Request):
        user: User = request.state.user
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        if not required_role:
            return user

        if required_role == Role.manager and not user.is_manager:  # type: ignore
            raise HTTPException(status_code=403, detail="Not enough permissions")

        # The manager can also view things that are for normal users
        # if required_role == Role.normal and user.is_manager:  # type: ignore
        #     raise HTTPException(status_code=403, detail="Mismatch permissions")

        return user
    return role_checker


# /app/middleware/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.model.user import User, create_user, get_user  # Ensure these functions are defined
from passlib.context import CryptContext

router = APIRouter()

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a User Sign-Up schema
class UserSignup(BaseModel):
    username: str
    password: str
    email: str

# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)

# Sign-Up endpoint
@router.post("/signup")
async def signup(user_data: UserSignup):
    # Check if the user already exists
    if get_user(username=user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user with hashed password
    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),  # Hash the password before saving
        email=user_data.email,
        role="normal"  # Default role for new users
    )

    # Save the new user in the database
    create_user(new_user)
    return {"message": "User created successfully"}

