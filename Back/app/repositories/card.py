from Back.app.models.buyer_owns_card import BuyerOwnsCard
from Back.app.models.card import Card


class CardRepository:
    def __init__(self, session):
        self.session = session

    def add(self, card_number, card_name, card_security_num, card_exp_date, id_buyer):
        card = Card(card_number, card_name, card_security_num, card_exp_date)
        buyer_owns_card = BuyerOwnsCard(card.id_card, id_buyer)
        self.session.add(card)
        self.session.add(buyer_owns_card)
        self.session.commit()
