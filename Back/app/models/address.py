from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = "Address"

    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    floor = Column(Integer)
    door = Column(String, nullable=False)
    adit_info = Column(String)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    orders = relationship("Order", back_populates="address")
    buyer_addresses = relationship("BuyerAddress", back_populates="address")
