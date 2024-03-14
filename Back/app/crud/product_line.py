from Back.app.models.product_line import ProductLine
from sqlalchemy.orm import Session

from Back.app.models.product_seller import ProductSeller


def add_product_line(session: Session, id_order, id_product_seller, quantity, subtotal):
    product_seller = (
        session.query(ProductSeller)
        .filter(ProductSeller.id_product_seller == id_product_seller)
        .first()
    )
    product_seller_quantity = product_seller.quantity
    exists_already = (
        session.query(ProductLine)
        .filter(
            (ProductLine.order == id_order)
            and (ProductLine.id_product_seller == id_product_seller)
        )
        .all()
    )
    if quantity > product_seller_quantity:
        raise Exception("Product seller cannot sell more items than those he owns")
    elif len(exists_already) > 0:
        raise Exception(
            "The product line trying to be introduced is already in the order"
        )
    else:
        product_line = ProductLine(id_order, id_product_seller, quantity, subtotal)
        session.add(product_line)
        session.commit()
        # related_order.total+=price*quantity
