from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.card import CardCreate, CardUpdate
from app.service.buyer import BuyerService
from app.models.card import Card
from app.crud_repository import CRUDRepository


class CardService:
    def __init__(self, session: Session, buyer_service: BuyerService):
        self.session = session
        self.card_repo = CRUDRepository(session=session, model=Card)
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

    def get_by_id(self, id) -> Card:
        if card := self.card_repo.get_by_id(id):
            return card

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {id} not found.",
        )

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

    def delete_by_id(self, card_id):
        self.get_by_id(card_id)
        self.card_repo.delete_by_id(card_id)

    def delete_all(self):
        self.card_repo.delete_all()
