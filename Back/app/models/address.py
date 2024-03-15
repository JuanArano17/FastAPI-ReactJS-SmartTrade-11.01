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

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', floor={self.floor}, door='{self.door}', adit_info='{self.adit_info}', city='{self.city}', postal_code='{self.postal_code}', country='{self.country}')"
