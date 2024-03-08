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

class ProductSeller(Base):
    __tablename__ = 'ProductSeller'

    id_product_seller = Column(Integer, primary_key=True,autoincrement=True)
    id_product = Column(Integer, ForeignKey('Product.id_product'))
    id_seller = Column(Integer, ForeignKey('Seller.id_seller'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipping_costs = Column(Float, nullable=False)

    def __init__(self, id_product, id_seller, quantity, price, shipping_costs):
        self.id_product = id_product
        self.id_seller = id_seller
        self.quantity = quantity
        self.price = price
        self.shipping_costs = shipping_costs

class ProductLine(Base):
    __tablename__ = 'ProductLine'

    id_product_line = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey('Order.id_order'))
    id_product_seller = Column(Integer, ForeignKey('ProductSeller.id_product_seller'))
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    def __init__(self, id_order, id_product_seller, quantity, subtotal):
        self.id_order = id_order
        self.id_product_seller = id_product_seller
        self.quantity = quantity
        self.subtotal = subtotal

class BuyerAddress(Base):
    pass

def add_address(session, street, floor, door, adit_info, city, postal_code, country, id_buyer):
    address=Address(street,floor,door, adit_info, city, postal_code, country)
    buyer_address=BuyerAddress(address.id_address,id_buyer)
    session.add(address)
    session.add(buyer_address)
    session.commit(address)

def assign_address(session, id_address, id_buyer):
    buyer_address=BuyerAddress(id_address, id_buyer)
    session.add(buyer_address)
    session.commit(buyer_address)

#must have a product line!
def add_order(session,id_buyer, id_card, id_address, order_date, total):
    order=Order(id_buyer, id_card, id_address, order_date, total)
    session.add(order)
    session.commit(order)

def add_card(session, card_number, card_name, card_security_num, card_exp_date, id_buyer):
    card=Card( card_number, card_name, card_security_num, card_exp_date)
    buyer_owns_card=BuyerOwnsCard(card.id_card, id_buyer)
    session.add(card)
    session.add(buyer_owns_card)
    session.commit(card)

def assign_card(session, id_card, id_buyer):
    buyer_owns_card=BuyerOwnsCard(id_card, id_buyer)
    session.add(buyer_owns_card)
    session.commit(buyer_owns_card)

def add_refund_product(session, id_product_line, quantity, refund_date):
    product_line=session.query(ProductLine).filter(id_product_line=ProductLine.id_product_line).first()
    quantity_product_line=product_line.quantity
    order=session.query(Order).filter(Order.id_order==product_line.id_order)
    date_difference=refund_date-order.order_date
    
    if(quantity>quantity_product_line):
        print('Unable to refund more items than were ordered')
    elif(date_difference>30):
        print('Unable to refund a product more than 30 days after it has been ordered')
    else:
        refund_product=RefundProduct(id_product_line, quantity, refund_date)
        session.add(refund_product)
        session.commit(refund_product)

def add_product_seller(session,id_product, id_seller, quantity, price, shipping_costs):
    exists_already=session.query(ProductSeller).filter((ProductSeller.id_seller==id_seller)and(ProductSeller.id_product==id_product)).all()
    
    if(len(exists_already)>0):
        print ('The seller already owns an instance of this product')
    elif(price<0):
        print ('Price cannot be negative')
    elif(shipping_costs<0):
        print('Shipping costs cannot be negative')
    elif(quantity<=0):
        print('Quantity cannot be negative or 0')
    else:
        product_seller=ProductSeller(id_product, id_seller, quantity, price, shipping_costs)
        session.add(product_seller)
        session.commit(product_seller)

def add_product_line(session, id_order, id_product_seller, quantity, subtotal):
    product_seller=session.query(ProductSeller).filter(ProductSeller.id_product_seller==id_product_seller).first()
    product_seller_quantity=product_seller.quantity
    exists_already=session.query(ProductLine).filter((ProductLine.order==id_order)and(ProductLine.id_product_seller==id_product_seller)).all()
    related_order=session.query(Order).filter(Order.id_order==id_order).first()
    price=product_seller.price
    if(quantity>product_seller_quantity):
        print('Product seller cannot sell more items than those he owns')
    elif(len(exists_already)>0):
        print('The product line trying to be introduced is already in the order')
    elif(subtotal<0):
        print('Subtotal cannot be smaller than 0')
    else:
        product_line=ProductLine( id_order, id_product_seller, quantity, subtotal)
        session.add(product_line)
        session.commit(product_line)
        #related_order.total+=price*quantity

db=""
engine=create_engine(db)
Base.metadata.create_all(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()