from sqlalchemy import Float, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class Review(Base):
    __tablename__ = "Review"

    id = mapped_column(Integer,primary_key=True)
    id_seller_product = mapped_column(
        Integer,
        ForeignKey(
            "SellerProduct.id", ondelete="CASCADE", name="fk_review_seller_product_id"
        ),
        index=True,
        nullable=False,
    )
    id_buyer = mapped_column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_review_buyer_id"),
        index=True,
        nullable=False,
    )
    stars = mapped_column(Integer, nullable=False)
    comment = mapped_column(String)

    seller_product = relationship("SellerProduct", back_populates="reviews")
    buyer = relationship("Buyer", back_populates="reviews")


    def __repr__(self):
        return f"Review(id={self.id}, id_seller_product={self.id_seller_product}, id_buyer={self.id_buyer}, stars={self.stars}, comment={self.comment})"
