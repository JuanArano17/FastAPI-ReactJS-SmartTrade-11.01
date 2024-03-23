from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.base import Base


class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"
