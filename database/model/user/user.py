from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.init import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_manager = Column(Boolean, default=False)
    # hashed_password = Column(String)
    rooms = relationship("Room", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    hotels = relationship("Hotel", back_populates="user")
