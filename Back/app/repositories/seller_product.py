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
            seller_product = SellerProduct(
                id_product, id_seller, quantity, price, shipping_costs
            )
            self.session.add(seller_product)
            self.session.commit()
