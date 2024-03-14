from Back.app.models.order import Order
from sqlalchemy.orm import Session


# must have a product line!!!
def add_order(session: Session, id_buyer, id_card, id_address, order_date, total):
    order = Order(id_buyer, id_card, id_address, order_date, total)
    session.add(order)
    session.commit()
