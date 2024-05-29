from sqlalchemy import Date, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class Card(Base):
    __tablename__ = "Card"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_buyer = mapped_column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_card_buyer_id"),
        nullable=False,
    )
    card_number = mapped_column(String, nullable=False)
    card_name = mapped_column(String, nullable=False)
    card_security_num = mapped_column(String, nullable=False)
    card_exp_date = mapped_column(Date, nullable=False)

    orders = relationship("Order", back_populates="card")
    buyer = relationship("Buyer", back_populates="cards")

    def __repr__(self):
        return f"Card(id={self.id}, card_number='{self.card_number}', card_name={self.card_name}, card_exp_date='{self.card_exp_date}', card_security_num='{self.card_security_num}', id_buyer='{self.id_buyer}')"