from sqlalchemy import BinaryExpression, select
from Back.app.models.buyer_owns_card import BuyerOwnsCard
from Back.app.models.card import Card


class CardRepository:
    def __init__(self, session):
        self.session = session

    def add(self, card_number, card_name, card_security_num, card_exp_date, id_buyer):
        try:
            card = Card(card_number, card_name, card_security_num, card_exp_date)
            buyer_owns_card = BuyerOwnsCard(card.id_card, id_buyer)
            self.session.add(card)
            self.session.add(buyer_owns_card)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            cards = self.session.query(Card).all()
            return cards
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Card, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Card)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, card_id, new_data):
        try:
            card = self.session.query(Card).filter_by(id=card_id).first()
            if card:
                for key, value in new_data.items():
                    setattr(card, key, value)
                self.session.commit()
            else:
                raise ValueError("Card not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, card_id):
        try:
            card = self.session.query(Card).filter_by(id=card_id).first()
            if card:
                self.session.delete(card)
                self.session.commit()
            else:
                raise ValueError("Card not found.")
        except Exception as e:
            self.session.rollback()
            raise e
