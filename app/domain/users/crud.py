from sqlalchemy.orm import Session

from app.domain.users import models, schemas
from app.security import get_password_hash


def create_user(db: Session, data: schemas.UserCreate):
    hashed_password = get_password_hash(data.password)
    user = models.User(
        username=data.username,
        hashed_password=hashed_password,
        is_active=data.is_active,
        is_superuser=data.is_superuser,
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
