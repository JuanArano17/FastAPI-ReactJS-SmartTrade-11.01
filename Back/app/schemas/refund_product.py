from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RefundProductBase(BaseModel):
    quantity: int = Field(gt=0)
    refund_date: datetime


class RefundProductCreate(RefundProductBase):
    pass


class RefundProduct(RefundProductBase):
    id: Optional[int] = None
    id_product_line: int

    class Config:
        orm_mode = True
