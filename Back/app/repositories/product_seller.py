from Back.app.models.product_seller import ProductSeller


class ProductSellerRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_product, id_seller, quantity, price, shipping_costs):
        exists_already = (
            self.session.query(ProductSeller)
            .filter(
                (ProductSeller.id_seller == id_seller)
                and (ProductSeller.id_product == id_product)
            )
            .all()
        )

        if len(exists_already) > 0:
            raise Exception("The seller already owns an instance of this product")
        else:
            product_seller = ProductSeller(
                id_product, id_seller, quantity, price, shipping_costs
            )
            self.session.add(product_seller)
            self.session.commit()
