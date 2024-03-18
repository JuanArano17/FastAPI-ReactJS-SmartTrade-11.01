from sqlalchemy import BinaryExpression, select
from Back.app.models.product import Product


class ProductRepository:
    def __init__(self, session):
        self.session = session

    def add(
        self, id_category, name, description, eco_points, spec_sheet, stock
    ):  # images? must have at least one
        try:
            product = Product(
                id_category, name, description, eco_points, spec_sheet, stock
            )
            self.session.add(product)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            products = self.session.query(Product).all()
            return products
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Product, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Product)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, seller_product_id, new_data):
        try:
            product = (
                self.session.query(Product).filter_by(id=seller_product_id).first()
            )
            if product:
                for key, value in new_data.items():
                    setattr(product, key, value)
                self.session.commit()
            else:
                raise ValueError("Product not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, product_id):
        try:
            product = self.session.query(Product).filter_by(id=product_id).first()
            if product:
                self.session.delete(product)
                self.session.commit()
            else:
                raise ValueError("Product not found.")
        except Exception as e:
            self.session.rollback()
            raise e
