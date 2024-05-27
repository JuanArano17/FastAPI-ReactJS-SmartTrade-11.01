from datetime import date, datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, FutureDate, NonNegativeFloat, validator

from app.schemas.orders.product_line import ProductLine, CompleteProductLine
from app.core.enums import OrderState, OrderType

class OrderBase(BaseModel):
    order_date: datetime = Field(default_factory=datetime.now)
    id_card: int 
    id_address: int
    state: OrderState
    total: NonNegativeFloat = Field(default=0)

    @validator("order_date")
    @classmethod
    def validate_date(cls, v: datetime):
        if v is not None and v.astimezone(timezone.utc) > datetime.now(tz=timezone.utc):
            raise ValueError("The order date must be in the past")
        return v

class OrderCreate(OrderBase):
    estimated_date: Optional[date] = None
    type: Optional[OrderType] = OrderType.STANDARD

class OrderUpdate(BaseModel):
    estimated_date: Optional[FutureDate] = None

class ConfirmOrder(BaseModel):
    id_address: int = None
    id_card: int = None
    type: Optional[OrderType] = OrderType.STANDARD


# Only used in populate_db.py
class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    id_address: Optional[int] = None
    id_card: Optional[int] = None
    estimated_date: Optional[FutureDate] = None

class ConfirmOrder(BaseModel):
    id_address: int = None
    id_card: int = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
    product_lines: list[ProductLine]


class CompleteOrder(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
    product_lines: list[CompleteProductLine]
    estimated_date: Optional[date] = None
    type: OrderType
