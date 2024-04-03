from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.service.user import UserService
from app.schemas.buyer import BuyerCreate, BuyerUpdate
from app.models.buyer import Buyer
from app.crud_repository import CRUDRepository
from app.core.security import get_password_hash


class BuyerRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Buyer)
        self._model = Buyer

    def get_by_email(self, email: str):  # -> Buyer | None:
        return self._db.query(self._model).filter(self._model.email == email).first()

    def get_by_dni(self, dni: str):  # -> Buyer | None:
        return self._db.query(self._model).filter(self._model.dni == dni).first()


class BuyerService:
    def __init__(self, session: Session, user_service: UserService):
        self.session = session
        self.buyer_repo = BuyerRepository(session=session)
        self.user_service = user_service

    def add(self, buyer: BuyerCreate) -> Buyer:
        if self.buyer_repo.get_by_dni(buyer.dni):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Buyer with dni {buyer.dni} already exists.",
            )

        if self.user_service.get_by_email(buyer.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {buyer.email} already exists.",
            )

        return self.buyer_repo.add(
            Buyer(
                **buyer.model_dump(exclude={"password"}),
                password=get_password_hash(buyer.password),
            )
        )

    def get_all(self) -> list[Buyer]:
        return self.buyer_repo.get_all()

    def get_by_id(self, id) -> Buyer:
        if buyer := self.buyer_repo.get_by_id(id):
            return buyer

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buyer with id {id} not found.",
        )

    def update(self, buyer_id, new_data: BuyerUpdate) -> Buyer:
        buyer = self.get_by_id(buyer_id)

        if new_data.email and self.user_service.get_by_email(new_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {buyer.email} already exists.",
            )

        if new_data.dni and self.buyer_repo.get_by_dni(new_data.dni):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Buyer with dni {new_data.dni} already exists.",
            )

        return self.buyer_repo.update(buyer, new_data)

    def delete_by_id(self, id):
        self.buyer_repo.get_by_id(id)
        self.buyer_repo.delete_by_id(id)

    def delete_all(self):
        self.buyer_repo.delete_all()
