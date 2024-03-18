from sqlalchemy import BinaryExpression, select
from Back.app.models.buyer_owns_card import Buyer


class BuyerRepository:
    def __init__(self, session):
        self.session = session

    # must have an address
    def add(
        self,
        email,
        name,
        surname,
        eco_points,
        password,
        dni,
        billing_address,
        payment_method,
    ):  # , id_addresses:list[Address]):
        try:
            buyer = Buyer(
                email,
                name,
                surname,
                eco_points,
                password,
                dni,
                billing_address,
                payment_method,
            )
            self.session.add(buyer)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            buyers = self.session.query(Buyer).all()
            return buyers
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Buyer, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Buyer)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e
