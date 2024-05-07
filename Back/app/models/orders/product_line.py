from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class ProductLine(Base):
    __tablename__ = "ProductLine"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_order = mapped_column(
        Integer,
        ForeignKey("Order.id", ondelete="CASCADE", name="fk_product_line_order_id"),
    )
    id_seller_product = mapped_column(
        Integer,
        ForeignKey(
            "SellerProduct.id",
            ondelete="CASCADE",
            name="fk_product_line_seller_product_id",
        ),
    )
    quantity = mapped_column(Integer, nullable=False)
    subtotal = mapped_column(Float, nullable=False)

    order = relationship("Order", back_populates="product_lines")
    seller_product = relationship("SellerProduct", back_populates="product_lines")
    refund_products = relationship(
        "RefundProduct", back_populates="product_line", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"ProductLine(id={self.id}, id_order={self.id_order}, id_seller_product={self.id_seller_product}, quantity={self.quantity}, subtotal={self.subtotal})"
