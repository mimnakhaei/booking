from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.init import Base


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    review_time = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="reviews")
    room = relationship("Room", back_populates="reviews")
