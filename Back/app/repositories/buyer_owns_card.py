from Back.app.models.buyer_owns_card import BuyerOwnsCard


class BuyerOwnsCardRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_card, id_buyer):
        try:
            buyer_owns_card = BuyerOwnsCard(id_card, id_buyer)
            self.session.add(buyer_owns_card)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            buyer_own_cards = self.session.query(BuyerOwnsCard).all()
            return buyer_own_cards
        except Exception as e:
            raise e
