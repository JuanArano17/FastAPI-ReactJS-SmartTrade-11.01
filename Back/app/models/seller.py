from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
#from app.database import Base
from app.base import Base

class Seller(Base):
    __tablename__ = "Seller"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    cif = Column(String(255), nullable=False, unique=True)
    bank_data = Column(String(255), nullable=False)

    seller_products = relationship(
        "SellerProduct", back_populates="seller", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Seller(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}', cif='{self.cif}', bank_data='{self.bank_data}')"
