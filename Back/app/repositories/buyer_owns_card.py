from sqlalchemy import BinaryExpression, select
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

    def get(self, pk):
        try:
            return self.session.get(BuyerOwnsCard, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(BuyerOwnsCard)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, buyer_id, new_data):
        try:
            buyer_owns_card = (
                self.session.query(BuyerOwnsCard).filter_by(id=buyer_id).first()
            )
            if buyer_owns_card:
                for key, value in new_data.items():
                    setattr(buyer_owns_card, key, value)
                self.session.commit()
            else:
                raise ValueError("Buyer card not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, buyer_id):
        try:
            buyer_owns_card = (
                self.session.query(BuyerOwnsCard).filter_by(id=buyer_id).first()
            )
            if buyer_owns_card:
                self.session.delete(buyer_owns_card)
                self.session.commit()
            else:
                raise ValueError("Buyer card not found.")
        except Exception as e:
            self.session.rollback()
            raise e
