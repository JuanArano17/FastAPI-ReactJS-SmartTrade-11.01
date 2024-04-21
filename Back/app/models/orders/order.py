from sqlalchemy import Date, Float, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from app.base import Base


class Order(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True, index=True)
    id_buyer = Column(
        Integer, ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_order_buyer_id")
    )
    id_card = Column(Integer, ForeignKey("Card.id", name="fk_order_card_id"))
    id_address = Column(Integer, ForeignKey("Address.id", name="fk_order_address_id"))
    order_date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)

    card = relationship("Card", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")

    product_lines = relationship(
        "ProductLine", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Order(id={self.id}, id_buyer={self.id_buyer}, id_card={self.id_card}, id_address={self.id_address}, order_date={self.order_date}, total={self.total})"