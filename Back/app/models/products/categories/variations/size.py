from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class Size(Base):
    __tablename__ = "Size"

    id = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    size = mapped_column(String(255), nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    seller_product_id = mapped_column(
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
