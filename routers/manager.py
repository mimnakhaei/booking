from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.hash import Hash
from schema import UserBase, UserDisplay

from auth import authenticate, Role
from database.init.db import get_db
from database.model.user.api import User, create_user, update_user, get_all_users, delete_user, get_user

router = APIRouter(prefix="/manager", tags=["Managers"])


@router.get("/users", response_model=list[UserDisplay])
def get_users(current_user: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    res: list[UserDisplay] = []
    for user in get_all_users(db):
        res.append(UserDisplay(id=user.id, username=user.username, email=user.email, password=user.password))  # type: ignore
    return res


@router.get("/users/{user_id}", response_model=UserDisplay)
def get_user_endpoint(user_id: int, current_user: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDisplay(id=user.id, username=user.username, email=user.email, password=user.password)  # type: ignore


@router.post("/users", response_model=UserDisplay)
def create_user_endpoint(request: UserBase, current_user: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    user = create_user(db, request)
    return UserDisplay(id=user.id, username=user.username, email=user.email, password=user.password)  # type: ignore


@router.delete("/users/{user_id}", response_model=dict)
def delete_user_endpoint(user_id: int, current_user: User = Depends(authenticate(Role.manager)), db: Session = Depends(get_db)):
    if delete_user(db, user_id):
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
