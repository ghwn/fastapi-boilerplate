from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.domain.subjects import models, schemas


def create_subject(db: Session, form: schemas.SubjectCreate) -> models.Subject:
    subject = models.Subject(name=form.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def get_subject_list(db: Session, offset: int = 0, limit: int = 100, **kwargs) -> List[models.Subject]:
    return db.query(models.Subject).filter_by(**kwargs).order_by(models.Subject.id).offset(offset).limit(limit).all()


def get_subject_by_id(db: Session, subject_id: int) -> models.Subject:
    return db.query(models.Subject).filter_by(id=subject_id).first()


def get_subject_by_name(db: Session, name: str) -> models.Subject:
    return db.query(models.Subject).filter_by(name=name).first()


def update_subject(db: Session, subject_id: int, form: schemas.SubjectUpdate) -> models.Subject:
    params = jsonable_encoder(form, by_alias=False, exclude_unset=False)
    subjects = db.query(models.Subject).filter_by(id=subject_id)
    subjects.update(params)
    subject = subjects.first()
    db.commit()
    db.refresh(subject)
    return subject


def patch_subject(db: Session, subject_id: int, form: schemas.SubjectPatch) -> models.Subject:
    params = jsonable_encoder(form, by_alias=False, exclude_unset=True)
    subjects = db.query(models.Subject).filter_by(id=subject_id)
    subjects.update(params)
    subject = subjects.first()
    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(db: Session, subject_id: int) -> None:
    subject = db.query(models.Subject).filter_by(id=subject_id).first()
    db.delete(subject)
    db.commit()
