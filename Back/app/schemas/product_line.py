from typing import Optional
from pydantic import BaseModel, Field


class ProductLineBase(BaseModel):
    quantity: int = Field(gt=0)
    subtotal: float = Field(ge=0)


class ProductLineCreate(ProductLineBase):
    pass


class ProductLine(ProductLineBase):
    id: Optional[int] = None
    id_order: int
    id_product_seller: int

    # refund_products: list[RefundProduct] = []

    class Config:
        orm_mode = True
