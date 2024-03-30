from sqlalchemy import Boolean, ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship
from app.base import Base


class Address(Base):
    __tablename__ = "Address"

    id = Column(Integer, primary_key=True, index=True)
    id_buyer = Column(
        Integer, ForeignKey("Buyer.id", ondelete="CASCADE"), nullable=False
    )
    street = Column(String, nullable=False)
    floor = Column(Integer)
    door = Column(String, nullable=False)
    adit_info = Column(String)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    default = Column(Boolean, nullable=False)

    orders = relationship("Order", back_populates="address")
    buyer = relationship("Buyer", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', floor={self.floor}, door='{self.door}', adit_info='{self.adit_info}', city='{self.city}', postal_code='{self.postal_code}', country='{self.country}')"
