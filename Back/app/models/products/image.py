from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from app.base import Base


class Image(Base):
    __tablename__ = "Image"

    id = mapped_column(Integer, primary_key=True, index=True)
    id_product = mapped_column(
        Integer,
        ForeignKey("Product.id", ondelete="CASCADE", name="fk_image_product_id"),
        nullable=False,
    )
    # should url be unique?
    url = mapped_column(String, nullable=False)

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"Image(id={self.id}, id_product='{self.id_product}', url='{self.url}')"
