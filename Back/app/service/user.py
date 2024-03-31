from sqlalchemy.orm import Session

from app.models.buyer import Buyer
from app.models.seller import Seller


# TODO: this is a temporary workaround to get buyers or sellers by their email, avoiding circular dependencies
# this is not the best approach, we should have a user table
class UserRepository:
    def __init__(self, *, session: Session) -> None:
        self._db = session

    def get_by_email(self, email: str) -> Buyer | Seller | None:
        buyer = self._db.query(Buyer).filter(Buyer.email == email).first()
        if buyer:
            return buyer

        seller = self._db.query(Seller).filter(Seller.email == email).first()
        if seller:
            return seller

        return None


class UserService:
    def __init__(self, *, session: Session) -> None:
        self._db = session
        self._user_repository = UserRepository(session=session)

    def get_by_email(self, email: str) -> Buyer | Seller | None:
        return self._user_repository.get_by_email(email=email)
