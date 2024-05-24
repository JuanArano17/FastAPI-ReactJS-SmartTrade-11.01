from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, validator

from app.schemas.orders.product_line import ProductLine, CompleteProductLine
from app.core.enums import OrderState


class ConfirmOrder(BaseModel):
    id_card: int
    id_address: int


class OrderBase(BaseModel):
    order_date: datetime | None = Field(default_factory=datetime.now)
    id_card: int | None
    id_address: int | None
    state: OrderState
    total: NonNegativeFloat = Field(default=0)

    @validator("order_date")
    @classmethod
    def validate_date(cls, v: datetime):
        if v is not None and v.astimezone(timezone.utc) > datetime.now(tz=timezone.utc):
            raise ValueError("The order date must be in the past")
        return v


# Only used in populate_db.py
class OrderCreate(OrderBase):
    pass


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
