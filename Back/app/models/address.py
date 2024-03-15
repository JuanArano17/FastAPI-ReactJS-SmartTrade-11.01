from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = "Address"

    id_address = Column("id_address", Integer, primary_key=True, autoincrement=True)
    street = Column("street", String, nullable=False)
    floor = Column("floor", Integer)
    door = Column("door", String, nullable=False)
    adit_info = Column("adit_info", String)
    city = Column("city", String, nullable=False)
    postal_code = Column("postal_code", String, nullable=False)
    country = Column("country", String, nullable=False)

    orders = relationship("Order", back_populates="address")
    buyer_addresses = relationship("BuyerAddress", back_populates="address")
