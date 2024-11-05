from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from auth import authenticate, Role
from database.init.db import get_db
from database.model.user import User
from schema import HotelBase, HotelDisplay, HotelBodyInput
import database.model.hotel.api as hotel_api
from schema.hotel import create_hotel_display

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/", response_model=List[HotelDisplay])
def get_all_hotels(user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    res: List[HotelDisplay] = []
    for hotel in hotel_api.get_all_hotels(db):
        item = create_hotel_display(hotel)
        res.append(item)
    return res


@router.get("/user", response_model=List[HotelDisplay])
def get_all_user_hotels(user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    res: List[HotelDisplay] = []
    for hotel in hotel_api.get_hotels_by_user_id(db, user.id):  # type: ignore
        item = create_hotel_display(hotel)
        res.append(item)

    return res


@router.get("/{hotel_id}", response_model=HotelDisplay)
def get_hotel(hotel_id: int, user: User = Depends(authenticate(Role.normal)), db: Session = Depends(get_db)):
    hotel = hotel_api.get_hotel(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return create_hotel_display(hotel)

# BELOW ENDPOINTS ARE FOR MANAGER NOT USER. SHOULD BE CHANGED


@router.post("/", response_model=dict)
def create_hotel(hotel: HotelBodyInput, manager: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    hotel_api.create_hotel(db, HotelMetaWithID(name=hotel.name, address=hotel.address, user_id=manager.id))  # type: ignore

    return {"detail": "Hotel created successfully"}


@router.put("/{hotel_id}", response_model=HotelDisplay)
def update_hotel(hotel_id: int, hotel: HotelBodyInput, manager: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    hotel_api.update_hotel(db, hotel_id, HotelBase(name=hotel.name, address=hotel.address, user_id=manager.id))  # type: ignore

    return {"detail": "Hotel updated successfully"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_api.delete_hotel(db, hotel_id)
    return {"detail": "Hotel deleted successfully"}
