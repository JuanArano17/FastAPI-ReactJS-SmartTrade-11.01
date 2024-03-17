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
