from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.products.product import Product


class Game(Product):
    __tablename__ = "Game"

    id = mapped_column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False,
        primary_key=True,
    )
    publisher = mapped_column(String(255), nullable=False)
    platform = mapped_column(String(255), nullable=False)
    size = mapped_column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Game",
    }

    def __repr__(self):
        return f"Game(id={self.id}, name='{self.name}', description='{self.description}', spec_sheet='{self.spec_sheet}', stock={self.stock}, publisher={self.publisher}, platform={self.platform}, size={self.size})"
