from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Image(Base):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(Integer, ForeignKey("Product.id"), nullable=False)
    url = Column(String)

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"Image(id={self.id}, id_product='{self.id_product}', url='{self.url}')"
