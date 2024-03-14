from Back.app.models.product_seller import ProductSeller
from sqlalchemy.orm import Session


def add_product_seller(
    session: Session, id_product, id_seller, quantity, price, shipping_costs
):
    exists_already = (
        session.query(ProductSeller)
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
        session.add(product_seller)
        session.commit()
