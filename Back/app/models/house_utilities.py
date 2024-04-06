from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.product import Product


class HouseUtilities(Product):
    __tablename__ = "HouseUtilities"

    id = Column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False, primary_key=True
    )
    brand = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "HouseUtilities",
    }

    def __repr__(self):
        return f"HouseUtilities(id={self.id}, id_category={self.id_category}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock}, brand={self.brand}, type={self.type})"