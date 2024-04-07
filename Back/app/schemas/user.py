from pydantic import BaseModel, ConfigDict, Field, EmailStr, NonNegativeFloat
from typing import List, Optional
from app.schemas.card import Card
from app.schemas.address import Address
from app.schemas.in_shopping_cart import InShoppingCart
from app.schemas.in_wish_list import InWishList
from app.schemas.order import Order


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=40)
    password: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    addresses: List[Address] = []
    in_shopping_cart: List[InShoppingCart] = []
    in_wish_list: List[InWishList] = []
    cards: List[Card] = []
    orders: List[Order] = []