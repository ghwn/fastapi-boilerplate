from fastapi import status

from app.exceptions.base import APIException


class AuthorizationFailedError(APIException):
    def __init__(self, detail: str = "Authorization has been failed."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class AccessDeniedError(APIException):
    def __init__(self, detail: str = "Not enough authority to access this resource."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
