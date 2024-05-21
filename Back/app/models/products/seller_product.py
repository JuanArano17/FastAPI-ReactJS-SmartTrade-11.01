from sqlalchemy import Boolean, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, mapped_column
from app.base import Base


class SellerProduct(Base):
    __tablename__ = "SellerProduct"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_product = mapped_column(
        Integer,
        ForeignKey(
            "Product.id", ondelete="CASCADE", name="fk_seller_product_product_id"
        ),
    )
    id_seller = mapped_column(
        Integer,
        ForeignKey("Seller.id", ondelete="CASCADE", name="fk_seller_product_seller_id"),
    )
    quantity = mapped_column(Integer, nullable=False)
    price = mapped_column(Numeric(10, 2), nullable=False)
    shipping_costs = mapped_column(Float, nullable=False)
    state = mapped_column(String, nullable=False)
    justification = mapped_column(String)
    eco_points = mapped_column(Float, nullable=False)
    age_restricted = mapped_column(Boolean)
    stars= mapped_column(Numeric(2,1))

    product = relationship("Product", back_populates="seller_products")
    in_wish_lists = relationship("InWishList", back_populates="seller_product")
    in_shopping_carts = relationship("InShoppingCart", back_populates="seller_product")
    seller = relationship("Seller", back_populates="seller_products")
    product_lines = relationship("ProductLine", back_populates="seller_product")
    sizes = relationship("Size", back_populates="seller_product")
    reviews = relationship("Review", back_populates="seller_product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"SellerProduct(id={self.id}, id_product={self.id_product}, id_seller={self.id_seller}, quantity={self.quantity}, price={self.price}, shipping_costs={self.shipping_costs}, state={self.state}, justification={self.justification}, eco_points={self.eco_points}, age_restricted={self.age_restricted})"

    def notify_observers(self, new_quantity: int):
        for cart_item in self.in_shopping_carts:
            # if self.sizes==[]:
            if cart_item.quantity > new_quantity:
                cart_item.quantity = new_quantity
        # else:
        #    pass
        # logic for clothes observer
