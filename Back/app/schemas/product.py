from typing import Optional
from pydantic import BaseModel, Field


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

    class Config:
        orm_mode = True
