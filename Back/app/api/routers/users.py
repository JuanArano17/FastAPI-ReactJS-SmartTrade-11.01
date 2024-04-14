from fastapi import APIRouter

from app.schemas.user import User
from app.api.deps import UserServiceDep
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User] | User)
async def read_users(user_service: UserServiceDep, email: EmailStr | None = None):
    if email:
        return user_service.get_by_email(email, exception=True)

    return user_service.get_all()


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, user_service: UserServiceDep):
    return user_service.get_by_id(user_id)
