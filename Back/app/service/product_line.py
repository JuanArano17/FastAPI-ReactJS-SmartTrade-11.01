from sqlalchemy.orm import Session
from app.models.product_line import ProductLine
from app.models.seller_product import SellerProduct
from Back.app.service.order import OrderService
from Back.app.service.seller_product import SellerProductService
from app.repository import Repository


class ProductLineService:
    def __init__(self, session: Session):
        self.session = session
        self.product_line_repo = Repository(session, ProductLine)

    def add_product_line(self, id_order, id_seller_product, quantity):
        try:
            seller_product_serv = SellerProductService(self.session)
            seller_product = seller_product_serv.filter_seller_products(
                SellerProduct.id_seller_product == id_seller_product
            ).first()
            seller_product_quantity = seller_product.quantity
            exists_already = self.filter_product_lines(
                ProductLine.order == id_order,
                ProductLine.id_seller_product == id_seller_product,
            )

            if quantity > seller_product_quantity:
                raise Exception(
                    "Product seller cannot sell more items than those he owns"
                )
            elif len(exists_already) > 0:
                raise Exception(
                    "The product line trying to be introduced is already in the order"
                )

            order_serv = OrderService(self.session)
            order = order_serv.get_order(id_order)
            order_serv.update_order(
                id_order, {"total": order.total + seller_product.price * quantity}
            )
            seller_product.quantity -= quantity
            subtotal = seller_product.price * quantity

            self.product_line_repo.add(
                id_order=id_order,
                id_seller_product=id_seller_product,
                quantity=quantity,
                subtotal=subtotal,
            )

        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_product_lines(self):
        try:
            return self.product_line_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_product_line(self, product_line_id):
        try:
            return self.product_line_repo.get(product_line_id)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_product_lines(self, *expressions):
        try:
            return self.product_line_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_product_line(self, product_line_id, new_data):
        try:
            product_line_instance = self.product_line_repo.get(product_line_id)
            # Check if the product line being updated is not already part of the order
            if "id_order" in new_data:
                new_order_id = new_data["id_order"]
                exists_already = self.filter_product_lines(
                    (ProductLine.order == new_order_id)
                    & (
                        ProductLine.id_seller_product
                        == product_line_instance.id_seller_product
                    )
                    & (
                        ProductLine.id != product_line_id
                    )  # Exclude the current product line
                )

                if len(exists_already) > 0:
                    raise Exception(
                        "The product line trying to be introduced is already in the order"
                    )

            if product_line_instance:
                if "quantity" in new_data:
                    new_quantity = new_data["quantity"]
                    seller_product_serv = SellerProductService(self.session)
                    seller_product = seller_product_serv.filter_seller_products(
                        SellerProduct.id_seller_product
                        == product_line_instance.id_seller_product
                    ).first()
                    seller_product_quantity = seller_product.quantity
                    existing_quantity = product_line_instance.quantity
                    available_quantity = seller_product_quantity + existing_quantity
                    if new_quantity > available_quantity:
                        raise Exception(
                            "Product seller cannot sell more items than those he owns"
                        )
                    else:
                        order_serv = OrderService(self.session)
                        order = order_serv.get_order(product_line_instance.id_order)
                        order_serv.update_order(
                            product_line_instance.id_order,
                            {
                                "total": order.total
                                + seller_product.price * new_quantity
                                - seller_product.price * existing_quantity
                            },
                        )
                        seller_product.quantity += existing_quantity
                        seller_product.quantity -= new_quantity
                        product_line_instance.subtotal = (
                            seller_product.price * new_quantity
                        )

                self.product_line_repo.update(product_line_instance, new_data)
                return product_line_instance
            else:
                raise ValueError("Product Line not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_product_line(self, product_line_id):
        try:
            product_line_instance = self.product_line_repo.get(product_line_id)
            if product_line_instance:
                self.product_line_repo.delete(product_line_instance)
            else:
                raise ValueError("Product Line not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
