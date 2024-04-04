from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.product import Product


class Game(Product):
    __tablename__ = "Game"

    id = Column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False, primary_key=True
    )
    publisher = Column(String(255), nullable=False)
    platform = Column(String(255), nullable=False)
    size = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Game",
    }

    def __repr__(self):
        return f"Game(id={self.id}, id_category={self.id_category}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock}, publisher={self.publisher}, platform={self.platform}, size={self.size})"