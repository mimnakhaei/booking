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


def create_review_display_list(reviews) -> list[ReviewDisplay]:
    return [
        ReviewDisplay(
            id=review.id,  # type: ignore
            content=review.content,  # type: ignore
            review_time=review.review_time,  # type: ignore
            user=UserMeta(username=review.user.username, email=review.user.email)
        )
        for review in reviews
    ]
