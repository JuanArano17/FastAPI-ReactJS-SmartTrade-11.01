from Back.app.models.buyer_owns_card import BuyerOwnsCard
from Back.app.models.card import Card
from sqlalchemy.orm import Session


def add_card(
    session: Session, card_number, card_name, card_security_num, card_exp_date, id_buyer
):
    card = Card(card_number, card_name, card_security_num, card_exp_date)
    buyer_owns_card = BuyerOwnsCard(card.id_card, id_buyer)
    session.add(card)
    session.add(buyer_owns_card)
    session.commit()
