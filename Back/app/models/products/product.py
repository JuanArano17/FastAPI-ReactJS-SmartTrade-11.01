from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.base import Base


class Product(Base):
    __tablename__ = "Product"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255))
    spec_sheet = mapped_column(String(255), nullable=False)
    stock = mapped_column(Integer, nullable=False)
    category = mapped_column(String, nullable=False)

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
