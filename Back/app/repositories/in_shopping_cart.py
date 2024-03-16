from Back.app.models.in_shopping_cart import InShoppingCart


class InShoppingCartRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_seller_product, id_buyer, quantity):
        in_shopping_cart = InShoppingCart(id_seller_product, id_buyer, quantity)
        self.session.add(in_shopping_cart)
        self.session.commit()
