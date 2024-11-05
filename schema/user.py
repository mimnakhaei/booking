from pydantic import BaseModel, EmailStr, root_validator
from typing import List


class UserMeta(BaseModel):
    username: str
    email: EmailStr


class UserBase(UserMeta):
    password: str


# It's the same as UserCreate, but it's used for signup
class UserSignup(UserBase):
    pass


# In UserSignIn, both username and email are optional but at least one of them must be provided
class UserSignIn(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str

    # Custom validation to ensure at least one of the fields is provided
    @root_validator(pre=True)
    def at_least_one_required(cls, values):
        if not (values.get('email') or values.get('username')):
            raise ValueError("Either email or username must be provided.")
        return values


class UserDisplay(UserBase):
    id: int
   # rooms: List["RoomDisplay"] = []  # type: ignore

    class Config:
        orm_mode = True


def create_user_display(user) -> UserDisplay:
    # Create UserDisplay model
    return UserDisplay(
        id=user.id,
        username=user.username,
        email=user.email,
        password=user.password  # Consider if you need to expose the password
    )
