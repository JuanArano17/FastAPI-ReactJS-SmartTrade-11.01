from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1, max_length=70)


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True
