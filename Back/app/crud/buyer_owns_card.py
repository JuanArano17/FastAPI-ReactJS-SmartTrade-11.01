from Back.app.models.buyer_owns_card import BuyerOwnsCard
from sqlalchemy.orm import Session


def assign_card(session: Session, id_card, id_buyer):
    buyer_owns_card = BuyerOwnsCard(id_card, id_buyer)
    session.add(buyer_owns_card)
    session.commit()
