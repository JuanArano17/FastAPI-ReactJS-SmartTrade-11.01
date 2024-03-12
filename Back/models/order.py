from sqlalchemy import DateTime, Float, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base=declarative_base()


class Order(Base):
    __tablename__ = 'Order'

    id_order = Column('id_order', Integer, primary_key=True, autoincrement=True)
    #id_buyer = Column('id_buyer', Integer, ForeignKey('Buyer.id_buyer'))
    id_card = Column('id_card', Integer, ForeignKey('Card.id_card'))
    id_address = Column('id_address',Integer, ForeignKey('Address.id_address'))
    order_date = Column('order_date', DateTime, nullable=False)
    total = Column('total', Float, nullable=False)

    card = relationship('Card', back_populates='orders')
    address = relationship('Address', back_populates='orders')
    #buyer= relaionship('Buyer', back_populates='orders')

    product_lines = relationship('ProductLine', back_populates='order')

#must have a product line!!!
def add_order(session,id_buyer, id_card, id_address, order_date, total):
    order=Order(id_buyer, id_card, id_address, order_date, total)
    session.add(order)
    session.commit()
