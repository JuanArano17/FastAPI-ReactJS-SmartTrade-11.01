from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.products.product import Product


class Clothes(Product):
    __tablename__ = "Clothes"

    id = mapped_column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False,
        primary_key=True,
    )
    materials = mapped_column(String(255), nullable=False)
    type = mapped_column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Clothes",
    }

    def __repr__(self):
        return f"Clothes(id={self.id}, name='{self.name}', description='{self.description}', spec_sheet='{self.spec_sheet}', stock={self.stock}, materials={self.materials}, type={self.type})"
