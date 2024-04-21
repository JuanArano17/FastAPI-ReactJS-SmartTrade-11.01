from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.models.users.types.user import User


class Buyer(User):
    __tablename__ = "Buyer"

    id = Column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE", name="fk_buyer_user_id"),
        primary_key=True,
        index=True,
    )
    eco_points = Column(Float, nullable=False)
    dni = Column(String(255), nullable=False, unique=True)
    billing_address = Column(String(255))
    payment_method = Column(String(255))

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
