from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.init import Base


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in = Column(DateTime)
    check_out = Column(DateTime)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
