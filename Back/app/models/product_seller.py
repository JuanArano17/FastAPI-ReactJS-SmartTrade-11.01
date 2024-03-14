from sqlalchemy import Float, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProductSeller(Base):
    __tablename__ = "ProductSeller"

    id_product_seller = Column(Integer, primary_key=True, autoincrement=True)
    # id_product = Column(Integer, ForeignKey('Product.id_product'))
    # id_seller = Column(Integer, ForeignKey('Seller.id_seller'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipping_costs = Column(Float, nullable=False)

    # product=relationship('Product', back_populates='product_sellers')
    # in_wish_list=relationship('InWishList', back_populates='product_sellers')
    # in_shopping_cart=relationship('InShoppingCart', back_populates='product_sellers')

    product_lines = relationship("ProductLine", back_populates="product_seller")
