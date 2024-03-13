from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


from Back.models.product_seller import ProductSeller

Base = declarative_base()


class ProductLine(Base):
    __tablename__ = "ProductLine"

    id_product_line = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey("Order.id_order"))
    id_product_seller = Column(Integer, ForeignKey("ProductSeller.id_product_seller"))
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="product_lines")
    product_seller = relationship("ProductSeller", back_populates="product_lines")

    refund_products = relationship("RefundProduct", back_populates="product_line")


def add_product_line(session, id_order, id_product_seller, quantity, subtotal):
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
