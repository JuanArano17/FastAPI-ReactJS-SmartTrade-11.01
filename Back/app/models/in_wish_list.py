from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class InWishList(Base):
    __tablename__ = "InWishList"

    id_product_seller = Column(
        Integer, ForeignKey("ProductSeller.id"), primary_key=True
    )
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), primary_key=True)

    buyer = relationship("Buyer", back_populates="in_wish_list")
    product_seller = relationship("ProductSeller", back_populates="in_wish_list")

    def __repr__(self):
        return f"InWishList(id_product_seller={self.id_product_seller}, id_buyer={self.id_buyer})"
