from fastapi import status


class APIException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class AuthorizationFailedError(APIException):
    def __init__(self, detail: str = "Authorization failed."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class AccessDeniedError(APIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough authority to access this resource.",
        )


class LoginFailedError(APIException):
    def __init__(self, detail: str = "Login failed."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


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
