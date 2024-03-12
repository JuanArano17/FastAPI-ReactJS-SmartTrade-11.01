from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base()

class BuyerOwnsCard(Base):
    __tablename__ = 'BuyerOwnsCard'

    id_card = Column(Integer, ForeignKey('Card.id_card'), primary_key=True)
    #id_buyer = Column(Integer, ForeignKey('Buyer.id_buyer'), primary_key=True)

    card = relationship('Card', back_populates='buyer_owns_cards')
    #buyer=relationship('Buyer', back_populates='buyer_owns_cards')

def assign_card(session, id_card, id_buyer):
    buyer_owns_card=BuyerOwnsCard(id_card, id_buyer)
    session.add(buyer_owns_card)
    session.commit()
