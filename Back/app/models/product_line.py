from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from app.database import Base


class ProductLine(Base):
    __tablename__ = "ProductLine"

    id = Column(Integer, primary_key=True, index=True)
    id_order = Column(Integer, ForeignKey("Order.id"))
    id_seller_product = Column(Integer, ForeignKey("SellerProduct.id"))
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="product_lines")
    seller_product = relationship("SellerProduct", back_populates="product_lines")
    refund_products = relationship(
        "RefundProduct", back_populates="product_line", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"ProductLine(id={self.id}, id_order={self.id_order}, id_seller_product={self.id_seller_product}, quantity={self.quantity}, subtotal={self.subtotal})"
