from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class User(UserBase):
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
