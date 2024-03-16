from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from database import Base


class ProductLine(Base):
    __tablename__ = "ProductLine"

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey("Order.id"))
    id_product_seller = Column(Integer, ForeignKey("ProductSeller.id"))
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="product_lines")
    product_seller = relationship("ProductSeller", back_populates="product_lines")

    refund_products = relationship("RefundProduct", back_populates="product_line")

    def __repr__(self):
        return f"ProductLine(id={self.id}, id_order={self.id_order}, id_product_seller={self.id_product_seller}, quantity={self.quantity}, subtotal={self.subtotal})"
