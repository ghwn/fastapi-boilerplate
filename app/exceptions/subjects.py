from fastapi import status

from app.exceptions.base import APIException


class SubjectAlreadyExistsError(APIException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The subject '{name}' already exist.",
        )


class SubjectDoesNotExistError(APIException):
    def __init__(self, subject_id: int = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The subject (id: {subject_id}) does not exist.",
        )
