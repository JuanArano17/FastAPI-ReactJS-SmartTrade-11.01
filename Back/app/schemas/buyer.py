from pydantic import BaseModel, ConfigDict, Field, EmailStr, NonNegativeFloat
from typing import List, Optional
from app.schemas.card import Card
from app.schemas.address import Address
from app.schemas.in_shopping_cart import InShoppingCart
from app.schemas.in_wish_list import InWishList
from app.schemas.order import Order


class BuyerBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    eco_points: NonNegativeFloat
    # TODO: change it later for a more formal validation
    dni: str = Field(min_length=9, max_length=9, pattern=r"^\d{8}[a-zA-Z]$")
    billing_address: str = Field(min_length=1, max_length=100)
    payment_method: str = Field(min_length=1, max_length=20)


class BuyerCreate(BuyerBase):
    password: str


class BuyerUpdate(BuyerBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=40)
    eco_points: Optional[NonNegativeFloat] = None
    # TODO: change it later for a more formal validation
    dni: Optional[str] = Field(
        default=None, min_length=9, max_length=9, pattern=r"^\d{8}[a-zA-Z]$"
    )
    billing_address: Optional[str] = Field(default=None, min_length=1, max_length=100)
    payment_method: Optional[str] = Field(default=None, min_length=1, max_length=20)
    password: Optional[str] = None


class Buyer(BuyerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    addresses: List[Address] = []
    in_shopping_cart: List[InShoppingCart] = []
    in_wish_list: List[InWishList] = []
    cards: List[Card] = []
    orders: List[Order] = []
