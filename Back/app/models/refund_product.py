from sqlalchemy import Date, DateTime, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from app.base import Base


class RefundProduct(Base):
    __tablename__ = "RefundProduct"

    id = Column(Integer, primary_key=True, index=True)
    id_product_line = Column(Integer, ForeignKey("ProductLine.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_date = Column(Date, nullable=False)

    product_line = relationship("ProductLine", back_populates="refund_products")

    def __repr__(self):
        return f"RefundProduct(id={self.id}, id_product_line={self.id_product_line}, quantity={self.quantity}, refund_date={self.refund_date})"
