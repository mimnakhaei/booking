from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.init.db import get_db
from schema import UserCreate, UserDisplay
from database.hash import Hash
from database.model.user.api import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
