from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr, validator


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: constr(
        strip_whitespace=True,
        to_lower=True,
        min_length=5,
        max_length=32,
    )
    password: str

    @validator("username")
    def username_must_start_with_alphabet(cls, username: str):
        if username[:1].isalpha():
            return username
        raise ValueError("username must start with alphabet.")


class UserUpdate(UserBase):
    password: str
    is_active: bool
    is_superuser: bool


class UserPatch(UserBase):
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]


class User(UserBase):
    id: int
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
