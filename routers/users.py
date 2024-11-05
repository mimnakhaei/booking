from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.hash import Hash

from database.model.user.api import User, create_user, update_user

from schema import UserBase, UserDisplay
from database.init.db import get_db
from auth import authenticate, Role

router = APIRouter(prefix="/user", tags=["Users"])

# region normal user endpoints


@router.get("/me", response_model=UserBase)
def get_me(user: User = Depends(authenticate(Role.normal))):
    return UserBase(username=user.username, email=user.email, password=user.password)  # type: ignore


@router.post("/me", response_model=UserBase)
def update_me(request: UserBase, user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    user = update_user(db, user.id, request)  # type: ignore

    return UserBase(username=user.username, email=user.email, password=user.password)  # type: ignore


@router.get("/bookings", response_model=None)  # TODO: choose response model
def get_bookings(user: User = Depends(authenticate(Role.normal))):
    # TODO: implement
    return None


@router.delete("/bookings/{booking_id}", response_model=None)  # TODO: choose response model
def delete_booking(booking_id: int, user: User = Depends(authenticate(Role.normal))):
    # TODO: implement
    return None

# endregion
