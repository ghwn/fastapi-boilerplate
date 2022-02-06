from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.domain.routes import APIRequestResponseLoggingRoute
from app.domain.users import crud, models, schemas
from app.exceptions import AccessDeniedError, UserAlreadyExistsError, UserDoesNotExistError

router = APIRouter(route_class=APIRequestResponseLoggingRoute)


@router.post("", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    form: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """Create new user."""
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
    """Get list of users."""
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
    """Get an individual user."""
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
    """Update an existing user."""
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
    """Partially update an existing user."""
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
    """Delete an existing user."""
    if not current_user.is_superuser and current_user.username != username:
        raise AccessDeniedError()
    user = crud.get_user_by_username(db, username)
    if not user:
        raise UserDoesNotExistError(username=username)
    crud.delete_user(db, username)
