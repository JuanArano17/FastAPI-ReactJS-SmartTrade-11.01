from typing import Optional
from pydantic import BaseModel, ConfigDict, FutureDate, NonNegativeFloat, NonNegativeInt
from app.schemas.orders.refund_product import RefundProduct
from app.schemas.products.categories.variations.size import Size


class ProductLineBase(BaseModel):
    quantity: NonNegativeInt
    subtotal: NonNegativeFloat


class ProductLineCreate(ProductLineBase):
    id_seller_product: int

class ProductLineUpdate(BaseModel):
    estimated_date:Optional[FutureDate]

class ProductLine(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    id_order: int
    id_seller_product: int
    refund_products: list[RefundProduct] = []
    id_size: Optional[int]=None


class CompleteProductLine(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_order: int
    id_seller_product: int
    name: str
    description: str
    category: str
    refund_products: list[RefundProduct] = []
    size: Optional[Size]=None
    estimated_date:Optional[FutureDate]
