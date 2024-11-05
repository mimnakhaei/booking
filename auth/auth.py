import base64
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, jwe
from enum import Enum

from database.model.user.api import get_user
from database.model.user import User
from database.init import get_db_directly
from config.config import settings

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

public_endpoints = ["/", "/signup", "/signin", "/docs", "/openapi.json"]

# Enum for User Roles


class Role(str, Enum):
    normal = "normal"
    manager = "manager"


# Class-based middleware for authentication. to verify the token and extract user
class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # The "/", signup and signin routes are public, so we skip authentication for them
        if request.url.path in public_endpoints:
            return await call_next(request)
        try:
            token = await oauth2_scheme(request)  # Use oauth2_scheme to extract token
            if token:
                # Decrypt the token sent by the client
                decrypted_token = jwe.decrypt(base64.urlsafe_b64decode(token), settings.JWE_SECRET_KEY)
                if not decrypted_token:
                    raise HTTPException(status_code=401, detail="Invalid token")

                # Decode the token to get claims (it checks the signature and expiration too)
                claims = jwt.decode(decrypted_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])  # type: ignore
                with get_db_directly() as db:
                    request.state.user = get_user(db, claims["user_id"])
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response


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

