from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.model.user.api import User
import database.model.user.api as user_api
import database.model.booking.api as booking_api
from schema import UserBase,  BookingDisplay
from database.init.db import get_db
from auth import authenticate, Role
from schema.booking import create_booking_display

router = APIRouter(prefix="/user", tags=["Users"])

# region normal user endpoints


@router.get("/me", response_model=UserBase)
def get_me(user: User = Depends(authenticate(Role.normal))):
    return UserBase(username=user.username, email=user.email, password=user.password)  # type: ignore


@router.post("/me", response_model=UserBase)
def update_me(request: UserBase, user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    user = user_api.update_user(db, user.id, request)  # type: ignore

    return UserBase(username=user.username, email=user.email, password=user.password)  # type: ignore


@router.get("/bookings", response_model=list[BookingDisplay])  # TODO: choose response model
def get_bookings(user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    res: list[BookingDisplay] = []
    bookings: list[booking_api.Booking] = booking_api.get_bookings_by_user_id(db, user.id)  # type: ignore
    for booking in bookings:
        res.append(create_booking_display(booking))
    return res


@router.delete("/bookings/{booking_id}", response_model=None)  # TODO: choose response model
def delete_booking(booking_id: int, user: User = Depends(authenticate(Role.normal))):
    # TODO: implement
    return None

# endregion
