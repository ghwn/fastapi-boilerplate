from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.domain.users import crud, models, schemas
from app.exceptions import AccessDeniedError, UserAlreadyExistsError, UserDoesNotExistError

router = APIRouter()


@router.post("", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    form: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    사용자를 생성합니다. 누구나 사용자를 새로 만들 수 있도록 별다른 인증을 요구하지 않습니다.
    """
    user = crud.get_user_by_username(db, form.username)
    if user:
        raise UserAlreadyExistsError(form.username)
    user = crud.create_user(db, form)
    return user


@router.get("", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
async def get_user_list(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    사용자 목록을 조회합니다. 슈퍼유저 권한이 요구됩니다.
    """
    if not current_user.is_superuser:
        raise AccessDeniedError()
    user_list = crud.get_user_list(db, offset, limit)
    return user_list


@router.get("/{username}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    특정 사용자를 조회합니다. 일반 유저는 자기 자신만 조회할 수 있으며 다른 사용자를 조회하려면 슈퍼유저 권한이 요구됩니다.
    """
    if not current_user.is_superuser and current_user.username != username:
        raise AccessDeniedError()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username)
    return user


@router.put("/{username}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def update_user(
    username: str,
    form: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    사용자를 수정합니다. 슈퍼유저 권한이 요구됩니다.
    """
    if not current_user.is_superuser:
        raise AccessDeniedError()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username=username)
    updated_user = crud.update_user(db, username, form)
    return updated_user


@router.patch("/{username}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def patch_user(
    username: str,
    form: schemas.UserPatch,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    사용자 정보 일부분을 수정합니다. 일반 유저는 자기 자신의 정보만 수정할 수 있습니다.
    단, `is_superuser` 필드를 수정하려면 슈퍼유저 권한이 있어야 합니다.
    """
    if not current_user.is_superuser and current_user.username != username:
        raise AccessDeniedError()
    if not current_user.is_superuser and form.is_superuser:
        raise AccessDeniedError()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username=username)
    patched_user = crud.patch_user(db, username, form)
    return patched_user


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    사용자를 삭제합니다. 자기 자신만 삭제할 수 있으며 다른 사용자를 삭제하려면 슈퍼유저 권한이 요구됩니다.
    """
    if not current_user.is_superuser and current_user.username != username:
        raise AccessDeniedError()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username=username)
    crud.delete_user(db, username)
