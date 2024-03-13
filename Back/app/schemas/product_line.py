from typing import Optional
from pydantic import BaseModel, Field
from Back.app.schemas.refund_product import RefundProduct


class ProductLine(BaseModel):
    id_product_line: Optional[int] = None
    id_order: int
    id_product_seller: int
    quantity: int = Field(gt=0)
    subtotal: float = Field(ge=0)
    refund_products: list[RefundProduct] = []

    class Config:
        orm_mode = True
