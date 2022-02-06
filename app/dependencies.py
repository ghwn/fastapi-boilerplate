from fastapi import Depends
from fastapi.security import APIKeyHeader
from jose.jwt import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.users.crud import get_user_by_username
from app.exceptions import InvalidAccessTokenError, InvalidAuthorizationHeaderError, UnsupportedTokenTypeError
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
        raise InvalidAuthorizationHeaderError()
    if token_type == "Bearer":
        try:
            claims = decode_access_token(access_token)
        except JWTError:
            raise InvalidAccessTokenError()
        try:
            username = claims["username"]
        except KeyError:
            raise InvalidAccessTokenError()
        user = get_user_by_username(db, username)
        return user
    raise UnsupportedTokenTypeError()
