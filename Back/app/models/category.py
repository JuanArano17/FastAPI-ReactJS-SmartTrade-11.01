from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"
