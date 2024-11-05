from pydantic import BaseModel
from datetime import datetime

from schema.review import create_review_display_list
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


def create_booking_display(booking) -> BookingDisplay:
    # Create UserDisplay model
    user_item = UserDisplay(
        id=booking.user.id,
        username=booking.user.username,
        email=booking.user.email,
        password=booking.user.password  # Consider if you need to expose the password
    )

    # Create RoomDisplay model with reviews
    room_item = RoomDisplay(
        id=booking.room.id,
        type=booking.room.type,
        room_number=booking.room.room_number,
        availability=booking.room.availability,
        hotel_id=booking.room.hotel_id,
        reviews=create_review_display_list(booking.room.reviews)
    )

    # Create BookingDisplay model
    return BookingDisplay(
        id=booking.id,  # type: ignore
        check_in=booking.check_in,  # type: ignore
        check_out=booking.check_out,  # type: ignore
        user=user_item,
        room=room_item
    )
