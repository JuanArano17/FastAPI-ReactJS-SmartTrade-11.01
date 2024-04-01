from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.seller_product import SellerProduct


class SellerBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    bank_data: str = Field(min_length=10, max_length=140)
    # TODO: change it later for a more formal validation
    cif: str = Field(pattern=r"^[A-Z][0-9]{8}$")


class SellerCreate(SellerBase):
    password: str


class SellerUpdate(SellerBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=40)
    bank_data: Optional[str] = Field(default=None, min_length=10, max_length=140)
    # TODO: change it later for a more formal validation
    cif: Optional[str] = Field(
        default=None, pattern=r"^[A-Z][0-9]{8}$"
    )


class Seller(SellerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seller_products: List[SellerProduct] = []
