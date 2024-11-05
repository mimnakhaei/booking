from pydantic import BaseModel
from typing import List

from .user import UserDisplay
from .room import RoomDisplay


class HotelBase(BaseModel):
    name: str
    address: str


class HotelCreate(HotelBase):
    user_id: int


class HotelDisplay(HotelBase):
    id: int
    user: UserDisplay
    rooms: List[RoomDisplay] = []

    class Config:
        orm_mode = True
