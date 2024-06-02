from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, Enum as EnumColumn
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base
from app.core.enums import OrderState, OrderType


class Order(Base):
    __tablename__ = "Order"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_buyer = mapped_column(
        Integer, ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_order_buyer_id")
    )
    id_card = mapped_column(Integer, ForeignKey("Card.id", name="fk_order_card_id"))
    id_address = mapped_column(
        Integer, ForeignKey("Address.id", name="fk_order_address_id")
    )
    order_date = mapped_column(DateTime)
    total = mapped_column(Numeric(10, 2), nullable=False)
    state = mapped_column(
        EnumColumn(OrderState), nullable=False, default=OrderState.CONFIRMED
    )
    type = mapped_column(
        EnumColumn(OrderType), nullable=False, default=OrderType.STANDARD
    )
    estimated_date = mapped_column(Date)

    card = relationship("Card", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")
   

    product_lines = relationship(
        "ProductLine", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Order(id={self.id}, id_buyer={self.id_buyer}, id_card={self.id_card}, id_address={self.id_address}, order_date={self.order_date}, total={self.total})"
