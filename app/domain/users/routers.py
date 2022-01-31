from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.users import crud, schemas

router = APIRouter()


@router.post("", response_model=schemas.User, status_code=201)
async def create_user(form: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, form.username)
    if user:
        raise HTTPException(status_code=400, detail=f"The user '{form.username}' already exists.")
    user = crud.create_user(db, form)
    return user


@router.get("", response_model=List[schemas.User], status_code=200)
async def get_user_list(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_list = crud.get_user_list(db, offset, limit)
    return user_list


@router.get("/{username}", response_model=schemas.User, status_code=200)
async def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"The user '{username}' does not exist.")
    return user
