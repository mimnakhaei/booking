from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.init.db import get_db
from schema import BookingCreate, BookingDisplay
import database.model.booking.api as booking_api

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post("/", response_model=BookingDisplay)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return booking_api.create_booking(db, booking)


@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = booking_api.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(db: Session = Depends(get_db)):
    return booking_api.get_all_bookings(db)


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_api.delete_booking(db, booking_id)
    return {"detail": "Booking deleted successfully"}
