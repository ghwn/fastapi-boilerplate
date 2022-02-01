from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.auth import schemas
from app.domain.users.crud import get_user_by_username
from app.exceptions.users import PasswordDoesNotMatchError, UserDoesNotExistError
from app.security import create_access_token, verify_password

router = APIRouter()


@router.post("/token", response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def create_token(form: schemas.LoginForm, db: Session = Depends(get_db)):
    """토큰을 발급합니다."""
    user = get_user_by_username(db, form.username)
    if not user:
        raise UserDoesNotExistError(username=form.username)
    if not verify_password(form.password, user.hashed_password):
        raise PasswordDoesNotMatchError()
    access_token = create_access_token({"username": user.username})
    return {"token_type": "Bearer", "access_token": access_token}
