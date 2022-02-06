from datetime import datetime, timedelta
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.configs import ACCESS_TOKEN_EXPIRATION_TIME, JWT_ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> Any:
    return pwd_context.hash(password)


def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = claims.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(access_token: str) -> dict:
    return jwt.decode(access_token, SECRET_KEY, [JWT_ALGORITHM])
