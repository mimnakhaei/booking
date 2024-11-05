from pydantic import BaseModel
from datetime import datetime
from .user import UserDisplay
from .room import RoomDisplay


class BookingBase(BaseModel):
    check_in: datetime
    check_out: datetime


class BookingCreate(BookingBase):
    user_id: int
    room_id: int


class BookingDisplay(BookingBase):
    id: int
    user: UserDisplay
    room: RoomDisplay

    class Config:
        orm_mode = True
