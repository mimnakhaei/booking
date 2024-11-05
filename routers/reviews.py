from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.init.db import get_db
from schema import ReviewCreate, ReviewDisplay
import database.model.review.api as review_api

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", response_model=ReviewDisplay)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return review_api.create_review(db, review)


@router.get("/{review_id}", response_model=ReviewDisplay)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = review_api.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.get("/", response_model=List[ReviewDisplay])
def get_all_reviews(db: Session = Depends(get_db)):
    return review_api.get_all_reviews(db)


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_api.delete_review(db, review_id)
    return {"detail": "Review deleted successfully"}
