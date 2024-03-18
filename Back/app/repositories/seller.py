from sqlalchemy import BinaryExpression, select
from Back.app.models.seller import Seller


class SellerRepository:
    def __init__(self, session):
        self.session = session

    def add(self, email, name, surname, password, cif, bank_data):
        try:
            seller = Seller(email, name, surname, password, cif, bank_data)
            self.session.add(seller)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            sellers = self.session.query(Seller).all()
            return sellers
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Seller, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Seller)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, seller_id, new_data):
        try:
            seller = self.session.query(Seller).filter_by(id=seller_id).first()
            if seller:
                for key, value in new_data.items():
                    setattr(seller, key, value)
                self.session.commit()
            else:
                raise ValueError("Seller not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, seller_id):
        try:
            seller = self.session.query(Seller).filter_by(id=seller_id).first()
            if seller:
                self.session.delete(seller)
                self.session.commit()
            else:
                raise ValueError("Seller not found.")
        except Exception as e:
            self.session.rollback()
            raise e
