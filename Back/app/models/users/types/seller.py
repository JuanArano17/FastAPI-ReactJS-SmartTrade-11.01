from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column

from app.models.users.types.user import User


class Seller(User):
    __tablename__ = "Seller"

    id = mapped_column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE", name="fk_seller_user_id"),
        primary_key=True,
        index=True,
    )
    birth_date = mapped_column(Date, nullable=False)
    cif = mapped_column(String(255), nullable=False, unique=True)
    bank_data = mapped_column(String(255), nullable=False)

    seller_products = relationship(
        "SellerProduct", back_populates="seller", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "Seller",
    }

    def __repr__(self):
        return f"Seller(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}', cif='{self.cif}', bank_data='{self.bank_data}')"
