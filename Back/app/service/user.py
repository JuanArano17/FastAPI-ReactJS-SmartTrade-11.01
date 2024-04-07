from sqlalchemy.orm import Session

from app.crud_repository import CRUDRepository
from app.models.user import User


class UserRepository(CRUDRepository):
    def __init__(self, *, session: Session) -> None:
        super().__init__(session=session, model=User)

    def get_by_email(self, email: str) -> User | None:
        return self._db.query(User).filter(User.email == email).first()
    

class UserService:
    def __init__(self, *, session: Session) -> None:
        self._db = session
        self._user_repository = UserRepository(session=session)

    def get_by_email(self, email: str) -> User | None:
        return self._user_repository.get_by_email(email=email)
