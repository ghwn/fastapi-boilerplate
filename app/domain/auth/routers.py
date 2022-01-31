from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.auth import schemas
from app.domain.users.crud import create_user, get_user_by_username
from app.domain.users.schemas import UserCreate
from app.security import create_access_token, verify_password

router = APIRouter()


@router.post("/signup", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
async def signup(form: schemas.SignupForm, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if user:
        raise HTTPException(status_code=400, detail=f"The user '{form.username}' already exists.")
    user = create_user(
        db,
        UserCreate(
            username=form.username,
            password=form.password,
            is_active=True,
            is_superuser=False,
        ),
    )
    access_token = create_access_token({"username": user.username})
    return {"token_type": "Bearer", "access_token": access_token}


@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def login(form: schemas.LoginForm, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if not user:
        raise HTTPException(status_code=404, detail=f"The user '{form.username}' does not exist.")
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail=f"Password does not match.")
    access_token = create_access_token({"username": user.username})
    return {"token_type": "Bearer", "access_token": access_token}
