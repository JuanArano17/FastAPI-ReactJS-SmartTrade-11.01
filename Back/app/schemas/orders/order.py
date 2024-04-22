from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, validator
from typing import List, Optional

from app.schemas.orders.product_line import ProductLine


class OrderBase(BaseModel):
    order_date: datetime = Field(default_factory=datetime.now)
    id_card: int
    id_address: int
    total: NonNegativeFloat = Field(default=0)

    @validator("order_date")
    @classmethod
    def validate_date(cls, v):
        if v > datetime.now():
            raise ValueError("The order date must be in the past")
        return v


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id_card: Optional[int] = None
    id_address: Optional[int] = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
    product_lines: List[ProductLine]
