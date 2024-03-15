from Back.app.models.buyer_owns_card import BuyerOwnsCard


class BuyerOwnsCardRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_card, id_buyer):
        buyer_owns_card = BuyerOwnsCard(id_card, id_buyer)
        self.session.add(buyer_owns_card)
        self.session.commit()
