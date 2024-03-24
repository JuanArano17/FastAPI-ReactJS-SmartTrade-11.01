from sqlalchemy.orm import Session
from app.models.product_line import ProductLine
from app.models.refund_product import RefundProduct
from Back.app.service.order import OrderService
from Back.app.service.product_line import ProductLineService
from app.repository import Repository


class RefundProductService:
    def __init__(self, session: Session):
        self.session = session
        self.refund_product_repo = Repository(session, RefundProduct)

    def add_refund_product(self, id_product_line, quantity, refund_date):
        try:
            # Retrieve product line and related order for validation
            product_line_serv = ProductLineService(self.session)
            product_line = product_line_serv.get_product_line(id_product_line)

            if not product_line:
                raise ValueError("Product line not found")

            order_line_serv = OrderService(self.session)
            order = order_line_serv.get_order(product_line.id_order)
            if not order:
                raise ValueError("Order not found")

            # Calculate date difference for validation
            date_difference = refund_date - order.order_date
            if date_difference.days > 30:
                raise ValueError(
                    "Unable to refund a product more than 30 days after it has been ordered"
                )
            elif date_difference.days < 0:
                raise ValueError("Invalid refund_date")

            # Validate quantity
            if quantity > product_line.quantity:
                raise ValueError("Unable to refund more items than were ordered")

            # Update quantities in related entities
            product_line.quantity -= quantity
            product_line.seller_product.quantity += quantity

            # Add refund product
            refund_product = self.refund_product_repo.add(
                id_product_line=id_product_line,
                quantity=quantity,
                refund_date=refund_date,
            )

            return refund_product
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_refund_products(self):
        try:
            return self.refund_product_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_refund_product(self, pk):
        try:
            return self.refund_product_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_refund_products(self, *expressions):
        try:
            return self.refund_product_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_refund_product(self, refund_product_id, new_data):
        try:
            refund_product_instance = self.refund_product_repo.get(refund_product_id)
            if refund_product_instance:
                product_line_id = new_data.get("id_product_line")
                quantity = new_data.get("quantity")
                refund_date = new_data.get("refund_date")

                if product_line_id or quantity or refund_date:
                    product_line = self.session.query(ProductLine).get(product_line_id)
                    if not product_line:
                        raise ValueError("Product line not found")

                    order = product_line.order
                    if not order:
                        raise ValueError("Order not found")

                    date_difference = refund_date - order.order_date

                    if quantity and quantity > product_line.quantity:
                        raise ValueError(
                            "Unable to refund more items than were ordered"
                        )
                    elif refund_date and date_difference.days > 30:
                        raise ValueError(
                            "Unable to refund a product more than 30 days after it has been ordered"
                        )
                    elif refund_date and date_difference.days < 0:
                        raise ValueError("Invalid refund date")

                self.refund_product_repo.update(refund_product_id, new_data)
                return refund_product_instance
            else:
                raise ValueError("Refund product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_refund_product(self, refund_product_id):
        try:
            refund_product_instance = self.refund_product_repo.get(refund_product_id)
            if refund_product_instance:
                self.refund_product_repo.delete(refund_product_id)
            else:
                raise ValueError("Refund product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
