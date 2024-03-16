from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from database import Base


class BuyerOwnsCard(Base):
    __tablename__ = "BuyerOwnsCard"

    id_card = Column(Integer, ForeignKey("Card.id"), primary_key=True)
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), primary_key=True)

    card = relationship("Card", back_populates="buyer_owns_cards")
    buyer = relationship("Buyer", back_populates="buyer_owns_cards")

    def __repr__(self):
        return f"BuyerOwnsCard(id_card={self.id_card}, id_buyer={self.id_buyer})"
