from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.subjects import crud, schemas
from app.exceptions import SubjectAlreadyExistsError, SubjectDoesNotExistError

router = APIRouter()


@router.post("", response_model=schemas.Subject, status_code=status.HTTP_201_CREATED)
async def create_subject(form: schemas.SubjectCreate, db: Session = Depends(get_db)):
    """서브젝트를 생성합니다."""
    subject = crud.get_subject_by_name(db, form.name)
    if subject:
        raise SubjectAlreadyExistsError(name=form.name)
    created_subject = crud.create_subject(db, form)
    return created_subject


@router.get("/{subject_id}", response_model=schemas.Subject, status_code=status.HTTP_200_OK)
async def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """서브젝트 단건을 조회합니다."""
    subject = crud.get_subject_by_id(db, subject_id)
    if not subject:
        raise SubjectDoesNotExistError(subject_id=subject_id)
    return subject


@router.get("", response_model=List[schemas.Subject], status_code=status.HTTP_200_OK)
async def get_subject_list(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """서브젝트 목록을 조회합니다."""
    return crud.get_subject_list(db, offset, limit)


@router.put("/{subject_id}", response_model=schemas.Subject, status_code=status.HTTP_200_OK)
async def update_subject(subject_id: int, form: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    """서브젝트를 수정합니다."""
    subject = crud.get_subject_by_id(db, subject_id)
    if not subject:
        raise SubjectDoesNotExistError(subject_id=subject_id)
    updated_subject = crud.update_subject(db, subject_id, form)
    return updated_subject


@router.patch("/{subject_id}", response_model=schemas.Subject, status_code=status.HTTP_200_OK)
async def patch_subject(subject_id: int, form: schemas.SubjectPatch, db: Session = Depends(get_db)):
    """서브젝트 일부분을 수정합니다."""
    subject = crud.get_subject_by_id(db, subject_id)
    if not subject:
        raise SubjectDoesNotExistError(subject_id=subject_id)
    patched_subject = crud.patch_subject(db, subject_id, form)
    return patched_subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """서브젝트를 삭제합니다."""
    subject = crud.get_subject_by_id(db, subject_id)
    if not subject:
        raise SubjectDoesNotExistError(subject_id=subject_id)
    crud.delete_subject(db, subject_id)
