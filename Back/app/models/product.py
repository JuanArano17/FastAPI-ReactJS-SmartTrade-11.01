from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    id_category = Column(Integer, ForeignKey("Category.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    eco_points = Column(Float, nullable=False)
    spec_sheet = Column(String(255), nullable=False)
    stock = Column(Integer, nullable=False)

    images = relationship("Image", back_populates="product")
    product_sellers = relationship("ProductSeller", back_populates="product")
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"Product(id={self.id}, id_category={self.id_category}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock})"
