from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from auth import authenticate, Role
from database.init.db import get_db
from database.model.user import User
from schema import BookingCreate, BookingDisplay
import database.model.booking.api as booking_api
import database.model.room.api as room_api
from schema.booking import create_booking_display

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(user: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    """Get all bookings. Only accessible by managers."""
    return [create_booking_display(item) for item in booking_api.get_all_bookings(db)]


@router.get("/user", response_model=List[BookingDisplay])
def get_all_user_bookings(user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    """Get all bookings for the authenticated user."""
    return [create_booking_display(item) for item in booking_api.get_bookings_by_user_id(db, user.id)]  # type: ignore


@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int, user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    """Get a specific booking by ID."""
    booking = booking_api.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return create_booking_display(booking)


@router.post("/", response_model=dict)
def create_booking(room_id: int = Body(..., embed=True), user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    """Create a new booking for a room."""
    if not room_api.get_room(db, room_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    booking = BookingCreate(user_id=user.id, room_id=room_id, check_in=datetime.now(), check_out=datetime.now())  # type: ignore
    booking_api.create_booking(db, booking)

    return {"detail": "Booking created successfully"}


@router.delete("/{booking_id}", response_model=dict)
def delete_booking(booking_id: int, user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    """Delete a booking. Users can only delete their own bookings."""
    booking = booking_api.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.user_id != user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this booking")
    booking_api.delete_booking(db, booking_id)
    return {"detail": "Booking deleted successfully"}
