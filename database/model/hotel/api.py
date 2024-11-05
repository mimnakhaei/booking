from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from database.model.room import Room
from schema import HotelBase
from database.model.user import User
from .hotel import Hotel


def create_hotel(db: Session, hotel: HotelBase) -> Hotel:
    db_hotel = Hotel(name=hotel.name, address=hotel.address, user_id=hotel.user_id)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def get_hotel(db: Session, hotel_id: int):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return hotel


def get_all_hotels(db: Session):
    # hotels =  db.query(Hotel).all()
    hotels = db.query(Hotel).options(
        joinedload(Hotel.user),  # Eager load the user relationship
        joinedload(Hotel.rooms),  # Eager load the rooms relationship
        joinedload(Hotel.rooms).joinedload(Room.reviews)  # Eager load the reviews relationship
    ).all()
    if not hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return hotels


def get_hotels_by_user_id(db: Session, user_id: int):
    hotels = db.query(Hotel).options(
        joinedload(Hotel.user),  # Eager load the user relationship
        joinedload(Hotel.rooms),  # Eager load the rooms relationship
        joinedload(Hotel.rooms).joinedload(Room.reviews)  # Eager load the reviews relationship
    ).filter(Hotel.user_id == user_id).all()
    if not hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return hotels


def update_hotel(db: Session, hotel_id: int, hotel: HotelBase):
    db_hotel = get_hotel(db, hotel_id)
    if db_hotel:
        db_hotel.name = hotel.name  # type: ignore
        db_hotel.address = hotel.address  # type: ignore
        db.commit()
        db.refresh(db_hotel)
    return db_hotel


def delete_hotel(db: Session, hotel_id: int):
    db_hotel = get_hotel(db, hotel_id)
    if db_hotel:
        db.delete(db_hotel)
        db.commit()
