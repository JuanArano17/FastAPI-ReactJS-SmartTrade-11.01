from sqlalchemy import DateTime, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RefundProduct(Base):
    __tablename__ = "RefundProduct"

    id = Column(Integer, primary_key=True)
    id_product_line = Column(Integer, ForeignKey("ProductLine.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_date = Column(DateTime, nullable=False)

    product_line = relationship("ProductLine", back_populates="refund_products")
