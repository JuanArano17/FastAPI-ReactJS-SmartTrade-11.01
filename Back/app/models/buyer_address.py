from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BuyerAddress(Base):
    __tablename__ = "BuyerAddress"

    id_address = Column(Integer, ForeignKey("Address.id"), primary_key=True)
    id_buyer = Column(Integer, ForeignKey("Buyer.id"), primary_key=True)
    default = Column(Boolean, nullable=False)

    buyer = relationship("Buyer", back_populates="buyer_addresses")
    address = relationship("Address", back_populates="buyer_addresses")

    def __repr__(self):
        return f"BuyerAddress(id_address={self.id_address}, id_buyer={self.id_buyer}, default={self.default})"
