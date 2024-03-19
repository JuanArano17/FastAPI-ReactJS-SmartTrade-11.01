from sqlalchemy import BinaryExpression, select
from Back.app.models.in_shopping_cart import InShoppingCart


class InShoppingCartRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_seller_product, id_buyer, quantity):
        try:
            in_shopping_cart = InShoppingCart(id_seller_product, id_buyer, quantity)
            self.session.add(in_shopping_cart)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            in_shopping_cart_items = self.session.query(InShoppingCart).all()
            return in_shopping_cart_items
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(InShoppingCart, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(InShoppingCart)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, buyer_id, new_data):
        try:
            in_shopping_cart = (
                self.session.query(InShoppingCart).filter_by(id=buyer_id).first()
            )
            if in_shopping_cart:
                for key, value in new_data.items():
                    setattr(in_shopping_cart, key, value)
                self.session.commit()
            else:
                raise ValueError("Shopping cart item not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, buyer_id):
        try:
            in_shopping_cart = (
                self.session.query(InShoppingCart).filter_by(id=buyer_id).first()
            )
            if in_shopping_cart:
                self.session.delete(in_shopping_cart)
                self.session.commit()
            else:
                raise ValueError("Shopping cart item not found.")
        except Exception as e:
            self.session.rollback()
            raise e
