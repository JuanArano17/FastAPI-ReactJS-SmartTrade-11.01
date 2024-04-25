from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.users.token import Token
from app.api.deps import UserServiceDep
from app.core.security import create_access_token, authenticate_user

router = APIRouter(tags=["Login"])


@router.post("/login/access-token")
async def login_access_token(
    user_service: UserServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(
        email=form_data.username, password=form_data.password, user_service=user_service
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return Token(access_token=create_access_token(user.email), token_type="bearer")
