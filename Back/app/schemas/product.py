from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    eco_points: float
    spec_sheet: str
    stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    id_category: int

    class Config:
        orm_mode = True
