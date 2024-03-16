from Back.app.models.seller import Seller


class SellerRepository:
    def __init__(self, session):
        self.session = session

    def add(self, email, name, surname, password, cif, bank_data):
        seller = Seller(email, name, surname, password, cif, bank_data)
        self.session.add(seller)
        self.session.commit()
