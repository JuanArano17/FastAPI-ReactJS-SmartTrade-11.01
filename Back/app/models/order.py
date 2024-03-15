from sqlalchemy import DateTime, Float, ForeignKey, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Order(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True)
    id_buyer = Column(Integer, ForeignKey("Buyer.id"))
    id_card = Column(Integer, ForeignKey("Card.id"))
    id_address = Column(Integer, ForeignKey("Address.id"))
    order_date = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)

    card = relationship("Card", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")

    product_lines = relationship("ProductLine", back_populates="order")
