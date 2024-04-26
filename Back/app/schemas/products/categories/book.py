from typing import List, Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveInt,
)

from app.schemas.products.image import Image
from app.schemas.products.seller_product import SellerProduct


class BookBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: NonNegativeInt = Field(default=0)
    author: str = Field(min_length=1, max_length=20)
    pages: PositiveInt = Field(lt=30000)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(default=None, min_length=1, max_length=240)
    stock: Optional[NonNegativeInt] = None
    author: Optional[str] = Field(default=None, min_length=1, max_length=20)
    pages: Optional[PositiveInt] = Field(default=None, lt=30000)


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: List[Image]
    seller_products: List[SellerProduct] = []
