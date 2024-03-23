from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base


class InWishList(Base):
    __tablename__ = "InWishList"

    id_seller_product = Column(
        Integer, ForeignKey("SellerProduct.id"), primary_key=True, index=True
    )
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), primary_key=True, index=True)

    buyer = relationship("Buyer", back_populates="in_wish_list")
    seller_products = relationship("SellerProduct", back_populates="in_wish_list")

    def __repr__(self):
        return f"InWishList(id_seller_product={self.id_seller_product}, id_buyer={self.id_buyer})"
