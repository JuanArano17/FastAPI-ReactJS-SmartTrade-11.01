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
