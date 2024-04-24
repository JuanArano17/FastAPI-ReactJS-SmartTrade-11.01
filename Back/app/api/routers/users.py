from fastapi import APIRouter
from pydantic import EmailStr

from app.schemas.users.types.buyer import Buyer
from app.schemas.users.types.seller import Seller
from app.schemas.users.types.user import User
from app.api.deps import CurrentUserDep, UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User] | User)
async def read_users(user_service: UserServiceDep, email: EmailStr | None = None):
    if email:
        return user_service.get_by_email(email, exception=True)

    return user_service.get_all()


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, user_service: UserServiceDep):
    return user_service.get_by_id(user_id)


@router.get("/me", response_model=User)
async def read_user_me(current_user: CurrentUserDep) -> Buyer | Seller:
    """ "
    Return current user
    """
    return current_user
