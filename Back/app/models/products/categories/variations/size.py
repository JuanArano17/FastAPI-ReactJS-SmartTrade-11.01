from sqlalchemy import Column, ForeignKey, Integer, String
from app.base import Base
from sqlalchemy.orm import relationship

class Size(Base):
    __tablename__ = "Size"

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    size = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    seller_product_id = Column(
        Integer,
        ForeignKey(
            "SellerProduct.id",
            ondelete="CASCADE",
            name="fk_size_seller_product_id",
        ),
    )

    seller_product = relationship("SellerProduct", back_populates="sizes")

    def __repr__(self):
        return f"Size(id={self.id}, size = {self.size}, quantity={self.quantity}, seller_product_id={self.seller_product_id})"
