from pydantic import BaseModel
from typing import List

from schema.review import create_review_display_list

from .user import UserDisplay, create_user_display
from .room import RoomDisplay, create_room_display


class HotelMeta(BaseModel):
    name: str
    address: str


class HotelBase(HotelMeta):
    user_id: int


class HotelBodyInput(HotelMeta):
    pass


class HotelDisplay(HotelMeta):
    id: int
    user: UserDisplay  # Owner
    rooms: List[RoomDisplay] = []

    class Config:
        orm_mode = True


def create_hotel_display(hotel) -> HotelDisplay:
    # Create UserDisplay model
    user_item = create_user_display(hotel.user)
    # Create RoomDisplay model
    rooms = []
    for room in hotel.rooms:
        # Create RoomDisplay model with reviews
        room_item = create_room_display(room)
        rooms.append(room_item)

    # Create HotelDisplay model
    hotel_item = HotelDisplay(
        id=hotel.id,
        name=hotel.name,
        address=hotel.address,
        user=user_item,
        rooms=rooms
    )
    return hotel_item
