from sqlalchemy.orm import Session
from app.models.product_line import ProductLine
from app.models.refund_product import RefundProduct
from Back.app.service.order import OrderService
from Back.app.service.product_line import ProductLineService
from app.repository import Repository
from service.seller_product import SellerProductService


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


            other_refunded=0
            refund_products=self.filter_refund_products(RefundProduct.id_product_line==id_product_line)
            for refund_product in refund_products:
                other_refunded+=refund_product.quantity


            # Validate quantity
            if (quantity + other_refunded)> product_line.quantity:
                raise ValueError("Unable to refund more items than were ordered")

            # Update quantities in related entities
            seller_product_serv=SellerProductService(self.session)
            seller_product_quantity=seller_product_serv.get_seller_product(product_line.id_seller_product).quantity
            new_quantity=seller_product_quantity+quantity
            seller_product_serv.update_seller_product(product_line.id_seller_product, {"quantity":new_quantity})
        

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

    #no update method because we don't update a refund's details after it's made

    def delete_refund_product(self, refund_product_id):
        try:
            refund_product_instance = self.refund_product_repo.get(refund_product_id)
            if refund_product_instance:
                seller_product_serv=SellerProductService(self.session)
                product_line_serv=ProductLineService(self.session)
                product_line=product_line_serv.get_product_line(refund_product_instance.id_product_line)
                seller_product_quantity=seller_product_serv.get_seller_product(product_line.id_seller_product).quantity
                new_quantity=seller_product_quantity-refund_product_instance.quantity
                self.refund_product_repo.delete(refund_product_instance)
                seller_product_serv.update_seller_product(product_line.id_seller_product, {"quantity":new_quantity})
            else:
                raise ValueError("Refund product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
