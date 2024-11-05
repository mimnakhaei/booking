from pydantic import BaseModel
from typing import List, Optional
from .review import ReviewDisplay, create_review_display_list
from .user import UserMeta


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
    user: Optional[UserMeta] = None  # Allow user to be None

    class Config:
        orm_mode = True


def create_room_display(room) -> RoomDisplay:
    reviews = create_review_display_list(room.reviews)
    user = None
    if room.user:
        user = UserMeta(username=room.user.username, email=room.user.email)
    return RoomDisplay(
        id=room.id,
        type=room.type,
        room_number=room.room_number,
        availability=room.availability,
        hotel_id=room.hotel_id,
        reviews=reviews,
        user=user
    )
