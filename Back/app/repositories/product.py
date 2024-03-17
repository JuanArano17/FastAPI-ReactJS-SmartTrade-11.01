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
