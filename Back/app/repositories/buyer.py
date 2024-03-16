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
