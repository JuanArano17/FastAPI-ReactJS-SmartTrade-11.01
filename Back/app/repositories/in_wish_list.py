from Back.app.models.in_wish_list import InWishList


class InWishListRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_seller_product, id_buyer):
        try:
            in_wish_list = InWishList(id_seller_product, id_buyer)
            self.session.add(in_wish_list)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            in_wish_list_items = self.session.query(InWishList).all()
            return in_wish_list_items
        except Exception as e:
            raise e
