from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.product import Product

class Book(Product):
    __tablename__ = "Book"

    id = Column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_product_id"),
        nullable=False, primary_key=True
    )
    pages = Column(Integer, nullable=False)
    author = Column(String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Book",
    }

    def __repr__(self):
        return f"Book(id={self.id}, id_category={self.id_category}, name='{self.name}', description='{self.description}', eco_points={self.eco_points}, spec_sheet='{self.spec_sheet}', stock={self.stock}, pages='{self.pages}', author='{self.author}')"
