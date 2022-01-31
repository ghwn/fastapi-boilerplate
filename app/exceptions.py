from fastapi import status


class APIException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class UserAlreadyExistsError(APIException):
    def __init__(self, username: str) -> None:
        detail = f"The user '{username}' already exists."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserDoesNotExistError(APIException):
    def __init__(self, username: str = None):
        detail = f"The user '{username}' does not exist."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class SubjectAlreadyExistsError(APIException):
    def __init__(self, name: str):
        detail = f"The subject '{name}' already exist."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class SubjectDoesNotExistError(APIException):
    def __init__(self, subject_id: int = None):
        detail = f"The subject (id: {subject_id}) does not exist."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
