from fastapi import status

from app.exceptions.base import APIException


class UserAlreadyExistsError(APIException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The user '{username}' already exists.",
        )


class UserDoesNotExistError(APIException):
    def __init__(self, username: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user '{username}' does not exist.",
        )


class PasswordDoesNotMatchError(APIException):
    def __init__(self, detail: str = "The password does not match."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
