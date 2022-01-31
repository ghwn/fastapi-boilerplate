from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.users import crud, schemas
from app.exceptions import UserAlreadyExistsError, UserDoesNotExistError

router = APIRouter()


# 일부러 @router.post 등록 안함
async def create_user(form: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form.username)
    if user:
        raise UserAlreadyExistsError(form.username)
    user = crud.create_user(db, form)
    return user


@router.get("", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
async def get_user_list(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_list = crud.get_user_list(db, offset, limit)
    return user_list


@router.get("/{username}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username)
    return user
