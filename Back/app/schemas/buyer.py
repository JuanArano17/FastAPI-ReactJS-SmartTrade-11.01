from pydantic import BaseModel, Field
from typing import List
from Back.app.schemas.address import Address
from Back.app.schemas.buyer_owns_card import BuyerOwnsCard
from Back.app.schemas.in_shopping_cart import InShoppingCart
from Back.app.schemas.in_wish_list import InWishList
from Back.app.schemas.order import Order


class BuyerBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    email: str = Field(
        min_length=1, max_length=320, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )  # EmailStr?
    eco_points: float = Field(ge=0)
    dni: str = Field(min_length=9, max_length=9, pattern=r"^\d{8}[a-zA-Z]$")
    billing_address: str = Field(min_length=1, max_length=100)
    payment_method: str = Field(min_length=1, max_length=20)


class BuyerCreate(BuyerBase):
    password: str
    pass


class Buyer(BuyerBase):
    id: int
    addresses: List[Address]
    in_shopping_cart: List[InShoppingCart] = []
    in_wish_list: List[InWishList] = []
    buyer_owns_cards: List[BuyerOwnsCard] = []
    orders: List[Order] = []

    class Config:
        orm_mode = True
