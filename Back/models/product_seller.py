from sqlalchemy import Float, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base()

class ProductSeller(Base):
    __tablename__ = 'ProductSeller'

    id_product_seller = Column(Integer, primary_key=True,autoincrement=True)
    #id_product = Column(Integer, ForeignKey('Product.id_product'))
    #id_seller = Column(Integer, ForeignKey('Seller.id_seller'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipping_costs = Column(Float, nullable=False)

    #product=relationship('Product', back_populates='product_sellers')
    #in_wish_list=relationship('InWishList', back_populates='product_sellers')
    #in_shopping_cart=relationship('InShoppingCart', back_populates='product_sellers')

    product_lines = relationship('ProductLine', back_populates='product_seller')

def add_product_seller(session,id_product, id_seller, quantity, price, shipping_costs):
    exists_already=session.query(ProductSeller).filter((ProductSeller.id_seller==id_seller)and(ProductSeller.id_product==id_product)).all()

    if(len(exists_already)>0):
        raise Exception('The seller already owns an instance of this product')
    else:
        product_seller=ProductSeller(id_product, id_seller, quantity, price, shipping_costs)
        session.add(product_seller)
        session.commit()
