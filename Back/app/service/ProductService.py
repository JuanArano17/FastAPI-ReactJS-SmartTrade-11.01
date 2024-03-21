from sqlalchemy.orm import Session
from Back.app.models.product import Product
from Back.app.service.ImageService import ImageService
from repository import Repository


class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.product_repo = Repository(session, Product)

    def add_product(
        self, id_category, name, description, eco_points, spec_sheet, stock, url_image
    ):
        try:
            product = self.product_repo.add(
                id_category=id_category,
                name=name,
                description=description,
                eco_points=eco_points,
                spec_sheet=spec_sheet,
                stock=stock,
            )

            image_serv = ImageService(self.session)
            # must add at least one initial image
            image_serv.add_image(product.id, url_image)
            return product
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_products(self):
        try:
            return self.product_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_product(self, pk):
        try:
            return self.product_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_products(self, *expressions):
        try:
            return self.product_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_product(self, product_id, new_data):
        try:
            product_instance = self.product_repo.get(product_id)
            if product_instance:
                self.product_repo.update(product_id, new_data)
                return product_instance
            else:
                raise ValueError("Product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_product(self, product_id):
        try:
            product_instance = self.product_repo.get(product_id)
            if product_instance:
                self.product_repo.delete(product_id)
            else:
                raise ValueError("Product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
