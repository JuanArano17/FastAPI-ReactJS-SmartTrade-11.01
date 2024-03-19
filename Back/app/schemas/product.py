from typing import List, Optional
from pydantic import BaseModel, Field

from Back.app.schemas.image import Image
from Back.app.schemas.seller_product import SellerProduct


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    eco_points: float = Field(ge=0)
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    id_category: int
    images: List[Image]
    seller_products: List[SellerProduct] = []

    class Config:
        orm_mode = True
