from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt

from app.schemas.image import Image
from app.schemas.seller_product import SellerProduct

class ElectronicsBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    eco_points: NonNegativeFloat
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: NonNegativeInt = Field(default=0)
    brand: str = Field(min_length=1, max_length=40)
    type: str = Field(min_length=1, max_length=20)
    capacity: str = Field(max_length=9, pattern=r'^(\d+(\.\d+)?)(\s*[GgMmKk][Bb])?$')

class ElectronicsCreate(ElectronicsBase):
    pass

class ElectronicsUpdate(ElectronicsBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=40)
    description: Optional[str] = None
    eco_points: Optional[NonNegativeFloat] = None
    spec_sheet: str = Field(default=None, min_length=1, max_length=240)
    stock: Optional[NonNegativeInt] = None
    brand: Optional[str] = Field(default=None, min_length=1, max_length=30)
    type: Optional[str] = Field(default=None, min_length=1, max_length=20)
    capacity: Optional[str] = Field(default=None, max_length=9, pattern=r'^(\d+(\.\d+)?)(\s*[GgMmKk][Bb])?$')

class Electronics(ElectronicsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: List[Image]
    seller_products: List[SellerProduct] = []