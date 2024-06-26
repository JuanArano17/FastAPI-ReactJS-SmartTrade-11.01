from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, PastDate

from app.schemas.products.seller_product import SellerProduct


class SellerBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    birth_date: PastDate
    bank_data: str = Field(min_length=10, max_length=140)
    # TODO: change it later for a more formal validation
    cif: str = Field(pattern=r"^[A-Z][0-9]{8}$")
    profile_picture: Optional[str] = None


class SellerCreate(SellerBase):
    password: str


class SellerUpdate(SellerBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=40)
    birth_date: Optional[PastDate]= None
    bank_data: Optional[str] = Field(default=None, min_length=10, max_length=140)
    cif: Optional[str] = Field(default=None, pattern=r"^[A-Z][0-9]{8}$")
    password: Optional[str] = None
    profile_picture: Optional[str] = None


class Seller(SellerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    seller_products: List[SellerProduct] = []
