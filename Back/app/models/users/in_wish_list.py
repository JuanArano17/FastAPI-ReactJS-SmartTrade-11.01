from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class InWishList(Base):
    __tablename__ = "InWishList"

    id_seller_product = mapped_column(
        Integer,
        ForeignKey(
            "SellerProduct.id",
            ondelete="CASCADE",
            name="fk_wish_list_seller_product_id",
        ),
        primary_key=True,
        index=True,
    )
    id_buyer = mapped_column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_wish_list_buyer_id"),
        primary_key=True,
        index=True,
    )

    buyer = relationship("Buyer", back_populates="in_wish_lists")
    seller_product = relationship("SellerProduct", back_populates="in_wish_lists")

    def __repr__(self):
        return f"InWishList(id_seller_product={self.id_seller_product}, id_buyer={self.id_buyer})"
