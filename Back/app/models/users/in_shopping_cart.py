from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class InShoppingCart(Base):
    __tablename__ = "InShoppingCart"

    id = mapped_column(Integer,primary_key=True)
    id_seller_product = mapped_column(
        Integer,
        ForeignKey(
            "SellerProduct.id", ondelete="CASCADE", name="fk_cart_seller_product_id"
        ),
        index=True,
        nullable=False,
    )
    id_buyer = mapped_column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_cart_buyer_id"),
        index=True,
        nullable=False,
    )
    quantity = mapped_column(Integer, nullable=False)
    id_size = mapped_column(Integer, ForeignKey("Size.id", ondelete="CASCADE", name="fk_cart_size_id"),)

    seller_product = relationship("SellerProduct", back_populates="in_shopping_carts")
    buyer = relationship("Buyer", back_populates="in_shopping_carts")


    def __repr__(self):
        return f"InShoppingCart(id_seller_product={self.id_seller_product}, id_buyer={self.id_buyer}, quantity={self.quantity})"
