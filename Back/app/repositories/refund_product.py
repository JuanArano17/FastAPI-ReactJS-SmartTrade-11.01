from Back.app.models.order import Order
from Back.app.models.product_line import ProductLine
from Back.app.models.refund_product import RefundProduct


class RefundProductRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_product_line, quantity, refund_date):
        product_line = (
            self.session.query(ProductLine)
            .filter(id_product_line=ProductLine.id_product_line)
            .first()
        )
        quantity_product_line = product_line.quantity
        order = self.session.query(Order).filter(
            Order.id_order == product_line.id_order
        )
        date_difference = refund_date - order.order_date

        if quantity > quantity_product_line:
            raise Exception("Unable to refund more items than were ordered")
        elif date_difference > 30:
            raise Exception(
                "Unable to refund a product more than 30 days after it has been ordered"
            )
        elif date_difference < 0:
            raise Exception("Invalid refund_date")
        else:
            try:
                refund_product = RefundProduct(id_product_line, quantity, refund_date)
                self.session.add(refund_product)
                refund_product.product_line.quantity = (
                    refund_product.product_line.quantity - quantity
                )
                refund_product.product_line.seller_product.quantity = (
                    refund_product.product_line.seller_product.quantity + quantity
                )
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e

    def list(self):
        try:
            refund_products = self.session.query(RefundProduct).all()
            return refund_products
        except Exception as e:
            raise e
