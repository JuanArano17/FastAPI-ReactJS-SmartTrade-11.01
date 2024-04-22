from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.crud_repository import CRUDRepository
from app.models.users.types.user import User


class UserRepository(CRUDRepository):
    def __init__(self, *, session: Session) -> None:
        super().__init__(session=session, model=User)

    def get_by_email(self, email: str) -> User | None:
        return self._db.query(User).filter(User.email == email).first()


class UserService:
    def __init__(self, *, session: Session) -> None:
        self._db = session
        self._user_repository = UserRepository(session=session)

    def get_all(self) -> list[User]:
        return self._user_repository.get_all()

    def get_by_email(self, email: str, exception: bool = False) -> User | None:
        user = self._user_repository.get_by_email(email=email)

        if not user and exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with email {email} not found",
            )

        return user

    def get_by_id(self, user_id: int) -> User:
        user = self._user_repository.get_by_id(id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with id {user_id} not found",
            )

        return user
