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
