from Back.app.models.in_wish_list import InWishList


class InWishListRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_seller_product, id_buyer):
        in_wish_list = InWishList(id_seller_product, id_buyer)
        self.session.add(in_wish_list)
        self.session.commit()
