from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose.jwt import JWTError

from app.database import SessionLocal
from app.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_bearer_token(auth_header: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if auth_header.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="The Authorization header is not Bearer token.")
    access_token = auth_header.credentials
    try:
        claims = decode_access_token(access_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return claims
