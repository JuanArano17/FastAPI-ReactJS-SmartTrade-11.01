from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional


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


# That doesn't seem to make sense. Not all users have these attributes, only buyers.
# class User(UserBase):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     addresses: List[Address] = []
#     in_shopping_cart: List[InShoppingCart] = []
#     in_wish_list: List[InWishList] = []
#     cards: List[Card] = []
#     orders: List[Order] = []


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
