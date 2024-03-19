from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import List, Optional

from Back.app.schemas.product_line import ProductLine


class OrderBase(BaseModel):
    order_date: datetime = Field(gt=date(2020, 1, 1))
    total: float = Field(ge=0)


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: Optional[int] = None
    id_buyer: int
    id_card: int
    id_address: int
    product_lines: List[ProductLine]

    class Config:
        orm_mode = True
