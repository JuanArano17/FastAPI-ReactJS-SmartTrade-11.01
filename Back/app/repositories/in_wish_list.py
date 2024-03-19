from sqlalchemy import BinaryExpression, select
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

    def get(self, pk):
        try:
            return self.session.get(InWishList, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(InWishList)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, buyer_id, new_data):
        try:
            in_wish_list = self.session.query(InWishList).filter_by(id=buyer_id).first()
            if in_wish_list:
                for key, value in new_data.items():
                    setattr(in_wish_list, key, value)
                self.session.commit()
            else:
                raise ValueError("Wish list item not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, buyer_id):
        try:
            in_wish_list = self.session.query(InWishList).filter_by(id=buyer_id).first()
            if in_wish_list:
                self.session.delete(in_wish_list)
                self.session.commit()
            else:
                raise ValueError("Wish list item not found.")
        except Exception as e:
            self.session.rollback()
            raise e
