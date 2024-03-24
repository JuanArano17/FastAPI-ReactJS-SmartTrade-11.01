from sqlalchemy import DateTime, ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship
from app.base import Base


class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True, index=True)
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), nullable=False)
    card_number = Column(String, nullable=False, unique=True)
    card_name = Column(String, nullable=False)
    card_security_num = Column(Integer, nullable=False)
    card_exp_date = Column(DateTime, nullable=False)

    orders = relationship("Order", back_populates="card")
    buyer = relationship("Buyer", back_populates="cards")
