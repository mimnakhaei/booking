from sqlalchemy.orm import Session
from schema import RoomCreate
from .room import Room


def create_room(db: Session, room: RoomCreate):
    db_room = Room(type=room.type, room_number=room.room_number, availability=room.availability, hotel_id=room.hotel_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()


def get_all_rooms(db: Session):
    return db.query(Room).all()


def update_room(db: Session, room_id: int, room: RoomCreate):
    db_room = get_room(db, room_id)
    if db_room:
        db_room.type = room.type  # type: ignore
        db_room.room_no = room.room_number
        db_room.availability = room.availability  # type: ignore
        db.commit()
        db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = get_room(db, room_id)
    if db_room:
        db.delete(db_room)
        db.commit()
