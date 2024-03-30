from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from app.base import Base


class SellerProduct(Base):
    __tablename__ = "SellerProduct"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(
        Integer,
        ForeignKey(
            "Product.id", ondelete="CASCADE", name="fk_seller_product_product_id"
        ),
    )
    id_seller = Column(
        Integer,
        ForeignKey("Seller.id", ondelete="CASCADE", name="fk_seller_product_seller_id"),
    )
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipping_costs = Column(Float, nullable=False)

    product = relationship("Product", back_populates="seller_products")
    in_wish_list = relationship("InWishList", back_populates="seller_products")
    in_shopping_cart = relationship("InShoppingCart", back_populates="seller_products")
    seller = relationship("Seller", back_populates="seller_products")
    product_lines = relationship("ProductLine", back_populates="seller_product")

    def __repr__(self):
        return f"SellerProduct(id={self.id}, id_product={self.id_product}, id_seller={self.id_seller}, quantity={self.quantity}, price={self.price}, shipping_costs={self.shipping_costs})"
