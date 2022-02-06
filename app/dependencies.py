from fastapi import Depends
from fastapi.security import APIKeyHeader
from jose.jwt import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.users.crud import get_user_by_username
from app.exceptions import AuthorizationFailedError
from app.security import decode_access_token

get_api_key = APIKeyHeader(name="Authorization")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    auth_header: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    try:
        token_type, access_token = auth_header.split(" ")
    except ValueError:
        raise AuthorizationFailedError(
            "Authorization header must consist of two parts: `token_type` and `access_token`."
        )
    if token_type == "Bearer":
        try:
            claims = decode_access_token(access_token)
        except JWTError:
            raise AuthorizationFailedError("Unable to parse JWT token.")
        try:
            username = claims["username"]
        except KeyError:
            raise AuthorizationFailedError("'username' field cannot be found on JWT claims.")
        user = get_user_by_username(db, username)
        return user
    raise AuthorizationFailedError("Unsupported token type")
