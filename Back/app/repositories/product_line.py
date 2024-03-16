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
            product_line = ProductLine(id_order, id_seller_product, quantity, subtotal)
            self.session.add(product_line)
            self.session.commit()
            # related_order.total+=price*quantity
