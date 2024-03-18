from select import select
from sqlalchemy import BinaryExpression
from Back.app.models.seller_product import SellerProduct


class SellerProductRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_product, id_seller, quantity, price, shipping_costs):
        exists_already = (
            self.session.query(SellerProduct)
            .filter(
                (SellerProduct.id_seller == id_seller)
                and (SellerProduct.id_product == id_product)
            )
            .all()
        )

        if len(exists_already) > 0:
            raise Exception("The seller already owns an instance of this product")
        else:
            try:
                seller_product = SellerProduct(
                    id_product, id_seller, quantity, price, shipping_costs
                )
                self.session.add(seller_product)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e

    def list(self):
        try:
            seller_products = self.session.query(SellerProduct).all()
            return seller_products
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(SellerProduct, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(SellerProduct)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, seller_product_id, new_data):
        try:
            seller_product = (
                self.session.query(SellerProduct)
                .filter_by(id=seller_product_id)
                .first()
            )
            if seller_product:
                for key, value in new_data.items():
                    setattr(seller_product, key, value)
                self.session.commit()
            else:
                raise ValueError("Seller product not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, seller_product_id):
        try:
            seller_product = (
                self.session.query(SellerProduct)
                .filter_by(id=seller_product_id)
                .first()
            )
            if seller_product:
                self.session.delete(seller_product)
                self.session.commit()
            else:
                raise ValueError("Seller product not found.")
        except Exception as e:
            self.session.rollback()
            raise e
