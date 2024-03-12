from sqlalchemy import DateTime, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from Back.models.order import Order

from Back.models.product_line import ProductLine

Base=declarative_base()

class RefundProduct(Base):
    __tablename__ = 'RefundProduct'

    id_refund_product=Column(Integer, primary_key=True, autoincrement=True)
    id_product_line = Column(Integer, ForeignKey('ProductLine.id_product_line'), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_date = Column(DateTime, nullable=False)

    product_line = relationship('ProductLine', back_populates='refund_products')

def add_refund_product(session, id_product_line, quantity, refund_date):
    product_line=session.query(ProductLine).filter(id_product_line=ProductLine.id_product_line).first()
    quantity_product_line=product_line.quantity
    order=session.query(Order).filter(Order.id_order==product_line.id_order)
    date_difference=refund_date-order.order_date

    if(quantity>quantity_product_line):
        raise Exception('Unable to refund more items than were ordered')
    elif(date_difference>30):
        raise Exception('Unable to refund a product more than 30 days after it has been ordered')
    elif(date_difference<0):
        raise Exception('Invalid refund_date')
    else:
        refund_product=RefundProduct(id_product_line, quantity, refund_date)
        session.add(refund_product)
        #subtract quantity from product line and add to product seller
        session.commit()
