from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base


class InShoppingCart(Base):
    __tablename__ = "InShoppingCart"

    id_seller_product = Column(
        Integer,
        ForeignKey(
            "SellerProduct.id", ondelete="CASCADE", name="fk_cart_seller_product_id"
        ),
        primary_key=True,
        index=True,
    )
    id_buyer = Column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_cart_buyer_id"),
        primary_key=True,
        index=True,
    )
    quantity = Column(Integer, nullable=False)

    seller_product = relationship("SellerProduct", back_populates="in_shopping_carts")
    buyer = relationship("Buyer", back_populates="in_shopping_carts")

    def __repr__(self):
        return f"InShoppingCart(id_seller_product={self.id_seller_product}, id_buyer={self.id_buyer}, quantity={self.quantity})"
        
    