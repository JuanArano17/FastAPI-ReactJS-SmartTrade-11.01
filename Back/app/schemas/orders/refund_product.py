from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from datetime import datetime


class RefundProductBase(BaseModel):
    quantity: PositiveInt
    # must be greater than order datetime
    refund_date: datetime = Field(default_factory=datetime.now)


class RefundProductCreate(RefundProductBase):
    pass


class RefundProduct(RefundProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product_line: int
