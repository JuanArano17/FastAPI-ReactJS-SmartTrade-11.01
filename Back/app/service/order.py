from sqlalchemy.orm import Session
from app.models.order import Order
from app.repository import Repository


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.order_repo = Repository(session, Order)

    def add_order(self, id_buyer, id_card, id_address, order_date):
        try:
            # should have at least one product line
            return self.order_repo.add(
                id_buyer=id_buyer,
                id_card=id_card,
                id_address=id_address,
                order_date=order_date,
                total=0,
            )

        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_orders(self):
        try:
            return self.order_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_order(self, order_id):
        try:
            return self.order_repo.get(order_id)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_orders(self, *expressions):
        try:
            return self.order_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_order(self, order_id, new_data):
        try:
            order_instance = self.order_repo.get(order_id)
            if order_instance:
                self.order_repo.update(order_instance, new_data)
                return order_instance
            else:
                raise ValueError("Order not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_order(self, order_id):
        try:
            order_instance = self.order_repo.get(order_id)
            if order_instance:
                self.order_repo.delete(order_instance)
            else:
                raise ValueError("Order not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
