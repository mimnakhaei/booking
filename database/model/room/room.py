from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.init import Base


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String)
    room_number = Column(String, unique=True)
    availability = Column(Boolean, default=True)

    hotel = relationship("Hotel", back_populates="rooms")
    user = relationship("User", back_populates="rooms")
    reviews = relationship("Review", back_populates="room")
    bookings = relationship("Booking", back_populates="room")
