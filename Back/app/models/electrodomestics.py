from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.product import Product


class Electrodomestics(Product):
    __tablename__ = "Electrodomestics"

    id = Column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False, primary_key=True
    )
    brand = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    power_source = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Electrodomestics",
    }

    def __repr__(self):
        return f"Electrodomestics(id={self.id}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock}, brand={self.brand}, type={self.type}, power_source={self.power_source})"