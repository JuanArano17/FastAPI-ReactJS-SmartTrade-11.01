from Back.app.models.order import Order


class OrderRepository:
    def __init__(self, session):
        self.session = session

    # must have a product line!!!
    def add(self, id_buyer, id_card, id_address, order_date, total):
        order = Order(id_buyer, id_card, id_address, order_date, total)
        self.session.add(order)
        self.session.commit()
