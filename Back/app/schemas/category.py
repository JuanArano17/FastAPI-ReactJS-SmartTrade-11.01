from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import Product


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=70)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    description: Optional[str] = Field(default=None, min_length=1, max_length=70)


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: List[Product] = []
