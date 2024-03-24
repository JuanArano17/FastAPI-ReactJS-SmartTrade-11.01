from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.seller_product import SellerProduct


class SellerBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    bank_data: str = Field(min_length=30, max_length=140)
    # TODO: change it later for a more formal validation
    cif: str = Field(pattern=r"^[A-HJNPQRSUVW]{1}[0-9]{7}[0-9A-J]$")


class SellerCreate(SellerBase):
    password: str


class Seller(SellerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seller_products: List[SellerProduct] = []
