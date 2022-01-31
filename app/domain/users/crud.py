from sqlalchemy.orm import Session

from app.domain.users import models, schemas
from app.security import get_password_hash


def create_user(db: Session, form: schemas.UserCreate):
    hashed_password = get_password_hash(form.password)
    user = models.User(
        username=form.username,
        hashed_password=hashed_password,
        is_active=form.is_active,
        is_superuser=form.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_list(db: Session, offset: int = 0, limit: int = 100, **kwargs):
    user_list = db.query(models.User).filter_by(**kwargs).order_by(models.User.id).offset(offset).limit(limit).all()
    return user_list


def get_user(db: Session, username: str):
    user = db.query(models.User).filter_by(username=username).first()
    return user
