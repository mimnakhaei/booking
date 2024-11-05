from pydantic import BaseModel
from datetime import datetime
from .user import UserMeta


class ReviewBase(BaseModel):
    content: str
    review_time: datetime | None = None


class ReviewCreate(ReviewBase):
    user_id: int
    room_id: int


class ReviewDisplay(ReviewBase):
    id: int
    user: UserMeta

    class Config:
        orm_mode = True
