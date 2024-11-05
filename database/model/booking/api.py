from sqlalchemy.orm import Session, joinedload
from database.model.review.review import Review
from database.model.room.room import Room
from schema import BookingCreate
from .booking import Booking


def create_booking(db: Session, booking: BookingCreate) -> Booking:
    db_booking = Booking(user_id=booking.user_id, room_id=booking.room_id, check_in=booking.check_in, check_out=booking.check_out)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int) -> Booking:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_all_bookings(db: Session) -> list[Booking]:
    return db.query(Booking).all()


def get_bookings_by_user_id(db: Session, user_id: int) -> list[Booking]:
    return db.query(Booking).options(joinedload(Booking.user), joinedload(Booking.room).joinedload(Room.reviews).joinedload(Review.user)).filter(Booking.user_id == user_id).all()


def delete_booking(db: Session, booking_id: int):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.delete(db_booking)
        db.commit()
