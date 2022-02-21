from typing import List, Optional

from app.domain.users import models, schemas
from app.security import get_password_hash
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


def create_user(db: Session, form: schemas.UserCreate):
    hashed_password = get_password_hash(form.password)
    user = models.User(
        username=form.username,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_list(db: Session, offset: int = 0, limit: int = 100, **kwargs) -> List[models.User]:
    user_list = (
        db.query(models.User)
        .filter_by(**kwargs)
        .order_by(models.User.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return user_list


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    user = db.query(models.User).filter_by(username=username).one_or_none()
    return user


def update_user(db: Session, username: str, form: schemas.UserUpdate) -> models.User:
    params = jsonable_encoder(form, by_alias=False, exclude_unset=False, exclude={"password"})
    params["hashed_password"] = get_password_hash(form.password)
    users = db.query(models.User).filter_by(username=username)
    users.update(params)
    user = users.first()
    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, username: str, form: schemas.UserPatch) -> models.User:
    params = jsonable_encoder(form, by_alias=False, exclude_unset=True, exclude={"password"})
    if form.password:
        params["hashed_password"] = get_password_hash(form.password)
    users = db.query(models.User).filter_by(username=username)
    users.update(params)
    user = users.first()
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str) -> None:
    user = db.query(models.User).filter_by(username=username).first()
    db.delete(user)
    db.commit()
