from sqlalchemy import DateTime, Float, create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base=declarative_base()

class Address(Base):
    __tablename__='Address'

    id_address=Column('id_address',Integer,primary_key=True,autoincrement=True)
    street=Column('street', String, nullable=False)
    floor=Column('floor', Integer)
    door=Column('door', String, nullable=False)
    adit_info=Column('adit_info', String)
    city=Column('city', String, nullable=False)
    postal_code=Column('postal_code', String, nullable=False)
    country=Column('country', String, nullable=False)

    def __init__(self, street, floor, door, adit_info, city, postal_code, country): 
        self.street=street
        self.floor=floor
        self.door=door
        self.adit_info=adit_info
        self.city=city
        self.postal_code=postal_code
        self.country=country

class Order(Base):
    __tablename__ = 'Order'

    id_order = Column('id_order',Integer, primary_key=True, autoincrement=True)
    id_buyer = Column('id_buyer',Integer, ForeignKey('Buyer.id_buyer'))
    id_card = Column('id_card', Integer, ForeignKey('Card.id_card'))
    id_address = Column('id_address',Integer, ForeignKey('Address.id_address'))
    order_date = Column('order_date', DateTime, nullable=False)
    total = Column('total', Float, nullable=False)

    def __init__(self, id_buyer, id_card, id_address, order_date, total):
        self.id_buyer = id_buyer
        self.id_card = id_card
        self.id_address = id_address
        self.order_date = order_date
        self.total = total

class Card(Base):
    __tablename__ = 'Card'

    id_card = Column(Integer, primary_key=True, autoincrement=True)
    card_number = Column(Integer, nullable=False)
    card_name = Column(String, nullable=False)
    card_security_num = Column(Integer, nullable=False)
    card_exp_date = Column(DateTime, nullable=False)

    def __init__(self, card_number, card_name, card_security_num, card_exp_date):
        self.card_number = card_number
        self.card_name = card_name
        self.card_security_num = card_security_num
        self.card_exp_date = card_exp_date


class BuyerOwnsCard(Base):
    __tablename__ = 'BuyerOwnsCard'

    id_card = Column(Integer, ForeignKey('Card.id_card'), primary_key=True)
    id_buyer = Column(Integer, ForeignKey('Buyer.id_buyer'), primary_key=True)

    def __init__(self, id_card, id_buyer):
        self.id_card = id_card
        self.id_buyer = id_buyer

class RefundProduct(Base):
    __tablename__ = 'RefundProduct'

    id_product_line = Column(Integer, ForeignKey('ProductLine.id_product_line'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    refund_date = Column(DateTime, nullable=False)

    def __init__(self, id_product_line, quantity, refund_date):
        self.id_product_line = id_product_line
        self.quantity = quantity
        self.refund_date = refund_date

