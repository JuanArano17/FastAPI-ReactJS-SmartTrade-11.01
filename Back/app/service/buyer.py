from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.buyer import BuyerCreate, BuyerUpdate
from app.models.buyer import Buyer
from app.crud_repository import CRUDRepository


class BuyerRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Buyer)
        self._model = Buyer

    def get_by_email(self, email: str) -> Buyer | None:
        self._db.query(self._model).filter(self._model.email == email).first()

    def get_by_dni(self, dni: str) -> Buyer | None:
        self._db.query(self._model).filter(self._model.dni == dni).first()


class BuyerService:
    def __init__(self, session: Session):
        self.session = session
        self.buyer_repo = BuyerRepository(session=session)

    def add(self, buyer: BuyerCreate) -> Buyer:
        if self.buyer_repo.get_by_dni(buyer.dni):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with dni {buyer.dni} already exists.",
            )

        if self.buyer_repo.get_by_email(buyer.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with email {buyer.email} already exists.",
            )

        return self.buyer_repo.add(Buyer(**buyer.model_dump()))

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

        if new_data.email and self.buyer_repo.get_by_email(new_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with email {new_data.email} already exists.",
            )

        if new_data.dni and self.buyer_repo.get_by_dni(new_data.dni):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with dni {new_data.dni} already exists.",
            )

        return self.buyer_repo.update(buyer, new_data)

    def delete_by_id(self, id):
        self.get_by_id(id)
        self.buyer_repo.delete_by_id(id)

    def delete_all(self):
        self.buyer_repo.delete_all()
