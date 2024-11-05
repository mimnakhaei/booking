# db/db_users.py
from sqlalchemy.orm import Session
from schema import UserCreate, UserSignup
from database.hash import Hash

from .user import User


def create_user(db: Session, user: UserCreate | UserSignup):
    hashed_password = Hash.bcrypt(user.password)  # Hashing the password
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user_id: int, user: UserCreate) -> User:
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user.username  # type: ignore
        db_user.email = user.email  # type: ignore
        db_user.hashed_password = user.password  # Ideally, hash the password before saving
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
