from typing import Optional
from pydantic import BaseModel, Field

from Back.app.schemas.refund_product import RefundProduct


class ProductLineBase(BaseModel):
    quantity: int = Field(gt=0)
    subtotal: float = Field(ge=0)


class ProductLineCreate(ProductLineBase):
    pass


class ProductLine(ProductLineBase):
    id: Optional[int] = None
    id_order: int
    id_seller_product: int
    refund_products: list[RefundProduct] = []

    class Config:
        orm_mode = True
