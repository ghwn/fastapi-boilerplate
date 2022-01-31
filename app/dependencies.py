from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose.jwt import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.users.crud import get_user_by_username
from app.exceptions import InvalidAccessTokenError, InvalidAuthorizationHeaderTypeError
from app.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    auth_header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if auth_header.scheme != "Bearer":
        raise InvalidAuthorizationHeaderTypeError()
    access_token = auth_header.credentials
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
