from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt

from app.schemas.products.image import Image
from app.schemas.products.seller_product import SellerProduct


class ClothesBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: NonNegativeInt = Field(default=0)
    materials: str = Field(min_length=1, max_length=40)
    type: str = Field(min_length=1, max_length=20)


class ClothesCreate(ClothesBase):
    pass


class ClothesUpdate(ClothesBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(default=None, min_length=1, max_length=240)
    stock: Optional[NonNegativeInt] = None
    materials: str = Field(default=None, min_length=1, max_length=40)
    type: str = Field(default=None, min_length=1, max_length=20)


class Clothes(ClothesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: List[Image]
    seller_products: List[SellerProduct] = []
