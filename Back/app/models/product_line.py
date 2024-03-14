from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
