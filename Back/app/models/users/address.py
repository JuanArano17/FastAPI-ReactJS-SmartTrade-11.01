from sqlalchemy import Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, mapped_column

from app.base import Base


class Address(Base):
    __tablename__ = "Address"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_buyer = mapped_column(
        Integer,
        ForeignKey("Buyer.id", ondelete="CASCADE", name="fk_address_buyer_id"),
        nullable=False,
    )
    street = mapped_column(String, nullable=False)
    floor = mapped_column(Integer)
    door = mapped_column(String, nullable=False)
    adit_info = mapped_column(String)
    city = mapped_column(String, nullable=False)
    postal_code = mapped_column(String, nullable=False)
    country = mapped_column(String, nullable=False)
    default = mapped_column(Boolean, nullable=False)

    orders = relationship("Order", back_populates="address")
    buyer = relationship("Buyer", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', floor={self.floor}, door='{self.door}', adit_info='{self.adit_info}', city='{self.city}', postal_code='{self.postal_code}', country='{self.country}')"
