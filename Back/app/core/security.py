from datetime import datetime, timedelta, UTC
from typing import Any
from passlib.context import CryptContext
from jose import jwt

from app.service.user import UserService
from app.models.users.types.user import User

# Temporary secret key for testing purposes
# This key should be replaced with a secure key in production
SECRET_KEY = "9c5edf7a9f2886eec424ce06bc564d1a5c7006fde292842e310f72e6f15227ee"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: str | Any, expires_delta: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    expire = datetime.now(tz=UTC) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(
    *, email: str, password: str, user_service: UserService
) -> User | None:
    user = user_service.get_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):  # type: ignore
        return None
    return user
