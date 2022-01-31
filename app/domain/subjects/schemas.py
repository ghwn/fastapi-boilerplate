from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class SubjectPatch(SubjectBase):
    name: Optional[str] = None


class Subject(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
