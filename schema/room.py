from pydantic import BaseModel
from typing import List, Optional
from .review import ReviewDisplay
from .user import UserBase


class RoomBase(BaseModel):
    type: str
    room_number: str
    availability: Optional[bool] = True


class RoomCreate(RoomBase):
    hotel_id: int


class RoomDisplay(RoomBase):
    id: int
    hotel_id: int
    reviews: List[ReviewDisplay] = []
    user: Optional[UserBase] = None  # Allow user to be None

    class Config:
        orm_mode = True
