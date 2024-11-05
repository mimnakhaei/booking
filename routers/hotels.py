from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.init.db import get_db
from schema import HotelCreate, HotelDisplay
import database.model.hotel.api as hotel_api
from schema.hotel import create_hotel_display

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/", response_model=List[HotelDisplay])
def get_all_hotels(db: Session = Depends(get_db)):
    res: List[HotelDisplay] = []
    for hotel in hotel_api.get_all_hotels(db):
        item = create_hotel_display(hotel)
        res.append(item)
    return res


@router.post("/", response_model=HotelDisplay)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    return hotel_api.create_hotel(db, hotel)


@router.get("/{hotel_id}", response_model=HotelDisplay)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = hotel_api.get_hotel(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return hotel


@router.put("/{hotel_id}", response_model=HotelDisplay)
def update_hotel(hotel_id: int, hotel: HotelCreate, db: Session = Depends(get_db)):
    return hotel_api.update_hotel(db, hotel_id, hotel)


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_api.delete_hotel(db, hotel_id)
    return {"detail": "Hotel deleted successfully"}
