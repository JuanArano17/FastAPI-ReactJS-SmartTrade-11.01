from sqlalchemy import BinaryExpression, select
from Back.app.models.product_line import ProductLine
from Back.app.models.seller_product import SellerProduct


class ProductLineRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_order, id_seller_product, quantity, subtotal):
        seller_product = (
            self.session.query(SellerProduct)
            .filter(SellerProduct.id_seller_product == id_seller_product)
            .first()
        )
        seller_product_quantity = seller_product.quantity
        exists_already = (
            self.session.query(ProductLine)
            .filter(
                (ProductLine.order == id_order)
                and (ProductLine.id_seller_product == id_seller_product)
            )
            .all()
        )
        if quantity > seller_product_quantity:
            raise Exception("Product seller cannot sell more items than those he owns")
        elif len(exists_already) > 0:
            raise Exception(
                "The product line trying to be introduced is already in the order"
            )
        else:
            try:
                product_line = ProductLine(
                    id_order, id_seller_product, quantity, subtotal
                )
                self.session.add(product_line)
                product_line.order.total += product_line.seller_product.price * quantity
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e

    def list(self):
        try:
            product_lines = self.session.query(ProductLine).all()
            return product_lines
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(ProductLine, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(ProductLine)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, product_line_id, new_data):
        try:
            product_line = (
                self.session.query(ProductLine).filter_by(id=product_line_id).first()
            )
            if product_line:
                for key, value in new_data.items():
                    setattr(product_line, key, value)
                self.session.commit()
            else:
                raise ValueError("Product Line not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, product_line_id):
        try:
            product_line = (
                self.session.query(ProductLine).filter_by(id=product_line_id).first()
            )
            if product_line:
                self.session.delete(product_line)
                self.session.commit()
            else:
                raise ValueError("Product Line not found.")
        except Exception as e:
            self.session.rollback()
            raise e
