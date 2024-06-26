from app.models.users.types.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.users.card import CardCreate, CardUpdate
from app.service.users.types.buyer import BuyerService
from app.models.users.card import Card
from app.crud_repository import CRUDRepository


class CardRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Card)
        self._model = Card

    def get_by_id_buyer(self, id_buyer) -> list[Card]:
        return (
            self._db.query(self._model).filter(self._model.id_buyer == id_buyer).all()
        )

    def delete_by_id_buyer(self, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()
        self._db.commit()


class CardService:
    def __init__(self, session: Session, buyer_service: BuyerService):
        self.session = session
        self.card_repo = CardRepository(session=session)
        self.buyer_service = buyer_service

    def add(self, id_buyer, card: CardCreate) -> Card:
        self.buyer_service.get_by_id(id_buyer)

        if self.card_repo.get_where(
            Card.card_number == card.card_number, Card.id_buyer == id_buyer
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Card with number {card.card_number} already exists for buyer with id {id_buyer}.",
            )

        card_obj = Card(**card.model_dump(), id_buyer=id_buyer)
        self.card_repo.add(card_obj)
        return card_obj

    def add_by_user(self, user: User, card: CardCreate) -> Card:
        self._check_is_buyer(user)
        return self.add(user.id, card)

    def get_by_id(self, id) -> Card:
        if card := self.card_repo.get_by_id(id):
            return card

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {id} not found.",
        )

    def get_one_by_user(self, user: User, card_id) -> Card:
        self._check_is_buyer(user)
        self._check_buyer_owns_card(user.id, card_id)
        return self.get_by_id(card_id)

    def get_by_id_buyer(self, id_buyer) -> list[Card]:
        return self.card_repo.get_by_id_buyer(id_buyer=id_buyer)

    def get_by_user(self, user: User) -> list[Card]:
        self._check_is_buyer(user)
        return self.get_by_id_buyer(user.id)

    def get_all(self) -> list[Card]:
        return self.card_repo.get_all()

    def update(self, card_id, new_data: CardUpdate) -> Card:
        card = self.get_by_id(card_id)

        if self.card_repo.get_where(
            Card.card_number == new_data.card_number,
            Card.id_buyer == card.id_buyer,
            Card.id != card_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Card with number {new_data.card_number} already exists for buyer with id {card.id_buyer}.",
            )

        return self.card_repo.update(card, new_data)

    def update_by_user(self, user: User, card_id, new_data: CardUpdate) -> Card:
        self._check_is_buyer(user)
        self._check_buyer_owns_card(user.id, card_id)
        return self.update(card_id, new_data)

    def delete_by_id(self, card_id):
        self.get_by_id(card_id)
        self.card_repo.delete_by_id(card_id)

    def delete_all(self):
        self.card_repo.delete_all()

    def delete_all_by_id_buyer(self, id_buyer):
        self.card_repo.delete_by_id_buyer(id_buyer=id_buyer)

    def delete_all_by_user(self, user: User):
        self._check_is_buyer(user)
        self.delete_all_by_id_buyer(user.id)

    def delete_one_by_user(self, card_id: int, user: User):
        self._check_is_buyer(user)
        self._check_buyer_owns_card(user.id, card_id)
        self.delete_by_id(card_id)

    def _check_is_buyer(self, user: User):
        if not str(user.type) == "Buyer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Users of type {user.type} do not have cards.",
            )

    def _check_buyer_owns_card(self, buyer_id, card_id):
        if not self.card_repo.get_where(Card.id == card_id, Card.id_buyer == buyer_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card with id {card_id} not found for buyer with id {buyer_id}.",
            )
