from sqlalchemy import DateTime, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from app.database import Base


class RefundProduct(Base):
    __tablename__ = "RefundProduct"

    id = Column(Integer, primary_key=True)
    id_product_line = Column(Integer, ForeignKey("ProductLine.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_date = Column(DateTime, nullable=False)

    product_line = relationship("ProductLine", back_populates="refund_products")

    def __repr__(self):
        return f"RefundProduct(id={self.id}, id_product_line={self.id_product_line}, quantity={self.quantity}, refund_date={self.refund_date})"
