from sqlalchemy import BinaryExpression, select
from Back.app.models.order import Order


class OrderRepository:
    def __init__(self, session):
        self.session = session

    # must have a product line!!!
    def add(
        self, id_buyer, id_card, id_address, order_date, total
    ):  # , product_line_ids: list[int]):
        try:
            order = Order(id_buyer, id_card, id_address, order_date, total)
            self.session.add(order)
            # self.session.add_all(product_line_ids)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            orders = self.session.query(Order).all()
            return orders
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Order, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Order)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, order_id, new_data):
        try:
            order = self.session.query(Order).filter_by(id=order_id).first()
            if order:
                for key, value in new_data.items():
                    setattr(order, key, value)
                self.session.commit()
            else:
                raise ValueError("Product Line not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, order_id):
        try:
            order = self.session.query(Order).filter_by(id=order_id).first()
            if order:
                self.session.delete(order)
                self.session.commit()
            else:
                raise ValueError("Product not found.")
        except Exception as e:
            self.session.rollback()
            raise e
