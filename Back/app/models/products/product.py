from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.base import Base


class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    spec_sheet = Column(String(255), nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Product",
        "polymorphic_on": category,
    }

    images = relationship(
        "Image", back_populates="product", cascade="all, delete-orphan"
    )
    seller_products = relationship(
        "SellerProduct",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', description='{self.description}', spec_sheet='{self.spec_sheet}', stock={self.stock}, type={self.category})"
