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
