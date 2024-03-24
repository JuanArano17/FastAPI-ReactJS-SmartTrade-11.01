from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import Product


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=70)


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: List[Product] = []
