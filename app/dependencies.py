from fastapi import Depends
from fastapi.security import APIKeyHeader
from jose.jwt import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domain.users.crud import get_user_by_username
from app.exceptions.auth import AuthorizationFailedError
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
        auth_type, credentials = auth_header.split(" ")
    except ValueError:
        raise AuthorizationFailedError(
            detail="Authorization header should consist of two parts:"
            " `auth type` and `credentials`.",
        )
    if auth_type == "Bearer":
        try:
            claims = decode_access_token(credentials)
        except JWTError:
            raise AuthorizationFailedError(detail="Unable to parse JWT token.")
        claim_name = "username"
        try:
            username = claims[claim_name]
        except KeyError:
            raise AuthorizationFailedError(
                detail=f"'{claim_name}' field is required in the JWT claims.",
            )
        user = get_user_by_username(db, username)
        return user
    raise AuthorizationFailedError(detail=f"'{auth_type}' is not supported auth type.")
