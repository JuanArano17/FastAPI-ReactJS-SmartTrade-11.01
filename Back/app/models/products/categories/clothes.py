from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.products.product import Product


class Clothes(Product):
    __tablename__ = "Clothes"

    id = Column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False,
        primary_key=True,
    )
    materials = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Clothes",
    }

    def __repr__(self):
        return f"Clothes(id={self.id}, name='{self.name}', description='{self.description}', spec_sheet='{self.spec_sheet}', stock={self.stock}, materials={self.materials}, type={self.type})"
