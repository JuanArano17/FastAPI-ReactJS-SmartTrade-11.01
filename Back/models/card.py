from sqlalchemy import DateTime, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database

from Back.models.buyer_owns_card import BuyerOwnsCard

Base=declarative_base()

class Card(Base):
    __tablename__ = 'Card'

    id_card = Column(Integer, primary_key=True, autoincrement=True)
    card_number = Column(String, nullable=False)
    card_name = Column(String, nullable=False)
    card_security_num = Column(Integer, nullable=False)
    card_exp_date = Column(DateTime, nullable=False)

    orders = relationship('Order', back_populates='card')
    buyer_owns_cards = relationship('BuyerOwnsCard', back_populates='card')

def add_card(session, card_number, card_name, card_security_num, card_exp_date, id_buyer):
    card=Card( card_number, card_name, card_security_num, card_exp_date)
    buyer_owns_card=BuyerOwnsCard(card.id_card, id_buyer)
    session.add(card)
    session.add(buyer_owns_card)
    session.commit()
