from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.products.product import Product


class Book(Product):
    __tablename__ = "Book"

    id = mapped_column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False,
        primary_key=True,
    )
    pages = mapped_column(Integer, nullable=False)
    author = mapped_column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Book",
    }

    def __repr__(self):
        return f"Book(id={self.id}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock}, pages='{self.pages}', author='{self.author}')"
