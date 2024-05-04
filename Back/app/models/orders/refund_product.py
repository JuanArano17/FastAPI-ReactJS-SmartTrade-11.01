from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class RefundProduct(Base):
    __tablename__ = "RefundProduct"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_product_line = mapped_column(
        Integer,
        ForeignKey(
            "ProductLine.id",
            ondelete="CASCADE",
            name="fk_refund_product_product_line_id",
        ),
        nullable=False,
    )
    quantity = mapped_column(Integer, nullable=False)
    refund_date = mapped_column(Date, nullable=False)

    product_line = relationship("ProductLine", back_populates="refund_products")

    def __repr__(self):
        return f"RefundProduct(id={self.id}, id_product_line={self.id_product_line}, quantity={self.quantity}, refund_date={self.refund_date})"
