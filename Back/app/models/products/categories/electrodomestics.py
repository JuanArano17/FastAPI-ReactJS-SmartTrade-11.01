from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.products.product import Product


class Electrodomestics(Product):
    __tablename__ = "Electrodomestics"

    id = mapped_column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False,
        primary_key=True,
    )
    brand = mapped_column(String(255), nullable=False)
    type = mapped_column(String(255), nullable=False)
    power_source = mapped_column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Electrodomestics",
    }

    def __repr__(self):
        return f"Electrodomestics(id={self.id}, name='{self.name}', description='{self.description}', spec_sheet='{self.spec_sheet}', stock={self.stock}, brand={self.brand}, type={self.type}, power_source={self.power_source})"
