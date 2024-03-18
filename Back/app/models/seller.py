from sqlalchemy import Column, Integer, String
from app.database import Base


class Seller(Base):
    __tablename__ = "Seller"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    cif = Column(String(255), nullable=False, unique=True)
    bank_data = Column(String(255), nullable=False)

    def __repr__(self):
        return f"Seller(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}', cif='{self.cif}', bank_data='{self.bank_data}')"
