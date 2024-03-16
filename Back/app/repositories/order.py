from Back.app.models.order import Order


class OrderRepository:
    def __init__(self, session):
        self.session = session

    # must have a product line!!!
    def add(
        self, id_buyer, id_card, id_address, order_date, total
    ):  # , product_line_ids: list[int]):
        order = Order(id_buyer, id_card, id_address, order_date, total)
        self.session.add(order)
        # self.session.add_all(product_line_ids)
        self.session.commit()
