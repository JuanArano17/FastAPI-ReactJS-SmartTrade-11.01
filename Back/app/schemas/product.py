from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt

from app.schemas.image import Image
from app.schemas.seller_product import SellerProduct


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    eco_points: NonNegativeFloat
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: NonNegativeInt


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_category: int
    images: List[Image]
    seller_products: List[SellerProduct] = []
