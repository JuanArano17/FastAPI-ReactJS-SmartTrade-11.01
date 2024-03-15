from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class InShoppingCart(Base):
    __tablename__ = "InShoppingCart"

    id_product_seller = Column(
        Integer, ForeignKey("ProductSeller.id"), primary_key=True
    )
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), primary_key=True)
    quantity = Column(Integer)

    product_seller = relationship("ProductSeller", back_populates="in_shopping_cart")
    buyer = relationship("Buyer", back_populates="in_shopping_cart")

    def __repr__(self):
        return f"InShoppingCart(id_product_seller={self.id_product_seller}, id_buyer={self.id_buyer}, quantity={self.quantity})"
