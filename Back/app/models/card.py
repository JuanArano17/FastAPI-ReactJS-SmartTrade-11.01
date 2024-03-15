from sqlalchemy import DateTime, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True)
    card_number = Column(String, nullable=False)
    card_name = Column(String, nullable=False)
    card_security_num = Column(Integer, nullable=False)
    card_exp_date = Column(DateTime, nullable=False)

    orders = relationship("Order", back_populates="card")
    buyer_owns_cards = relationship("BuyerOwnsCard", back_populates="card")
