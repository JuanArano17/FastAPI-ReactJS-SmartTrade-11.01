from sqlalchemy import Date, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapped_column

from app.models.users.types.user import User


class Buyer(User):
    __tablename__ = "Buyer"

    id = mapped_column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE", name="fk_buyer_user_id"),
        primary_key=True,
        index=True,
    )
    birth_date = mapped_column(Date, nullable=False)
    eco_points = mapped_column(Float, nullable=False)
    dni = mapped_column(String(255), nullable=False, unique=True)
    billing_address = mapped_column(String(255))
    payment_method = mapped_column(String(255))

    addresses = relationship(
        "Address", back_populates="buyer", cascade="all, delete-orphan"
    )
    in_shopping_carts = relationship(
        "InShoppingCart", back_populates="buyer", cascade="all, delete-orphan"
    )
    in_wish_lists = relationship(
        "InWishList", back_populates="buyer", cascade="all, delete-orphan"
    )
    cards = relationship("Card", back_populates="buyer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "Buyer",
    }

    def __repr__(self):
        return f"Buyer(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', eco_points={self.eco_points}, password='{self.password}', dni='{self.dni}', billing_address='{self.billing_address}', payment_method='{self.payment_method}')"
