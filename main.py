import base64
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt, jwe

from database.init import engine, Base, get_db
from database.model.user.api import create_user, get_user_by_username, get_user_by_email
from routers import users, hotels, rooms, reviews, bookings
from auth import AuthenticationMiddleware
from database.hash import Hash
from config import settings
from schema import UserSignup, UserSignIn

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Hotel Booking API', description='A Simple Hotel Booking API', version='0.0.1')

app.add_middleware(AuthenticationMiddleware)


# Public routes(endpoints)

@app.get("/")
def index():
    return {"message": "Hi There, I'm Alive :)))))"}


@app.post("/signup")
def signup(request: UserSignup, db: Session = Depends(get_db)):
    # Check user exists with sent username/email or not
    exists = get_user_by_username(db, request.username) or get_user_by_email(db, request.email)
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    user = create_user(db, request)
    if not user:
        raise HTTPException(status_code=500, detail="User creation failed")

    # Signup successful
    return {"message": "You have successfully signed up :)))))"}


@app.post("/signin")
def signin(request: UserSignIn, db: Session = Depends(get_db)):
    # Check user exists with sent username/email or not
    user = get_user_by_username(db, request.username) if request.username else get_user_by_email(db, request.email)  # type: ignore
    if not user:
        raise HTTPException(status_code=400, detail="Username/Email or password is incorrect")

    # Check password is correct or not
    if not Hash.verify(request.password, user.password):  # type: ignore
        raise HTTPException(status_code=400, detail="Username/Email or password is incorrect")

    # NOTICE:
    # Signin successfully happened, now we should generate a unique token for user and return it
    # For this, we generate a encrypted JWT token(JWE) and return it
    # We encrypt it because we don't want to the client(user) or anyone, be able to modify the token

    # This is the data that we want to store in the token (it will be encrypted ofcourse)
    claims = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_TIME_MINUTES)
    }
    # Create the JWT
    jwt_token = jwt.encode(claims, settings.JWT_SECRET_KEY, algorithm="HS256")
    # Encrypt the JWT
    encrypted_token = jwe.encrypt(jwt_token, str(settings.JWE_SECRET_KEY).encode(), algorithm="A256GCM", encryption="A256GCM")

    return {
        "message": "You have successfully signed in. Use your access token in further requests",
        "access_token": base64.urlsafe_b64encode(encrypted_token).decode(),
        # "token_type": "bearer"
    }


# Include isolated routers(endpoints)
app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(reviews.router)
app.include_router(bookings.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
