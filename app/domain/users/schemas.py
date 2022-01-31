from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
