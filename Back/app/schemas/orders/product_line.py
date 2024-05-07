from pydantic import BaseModel, ConfigDict, NonNegativeFloat, NonNegativeInt
from app.schemas.orders.refund_product import RefundProduct


class ProductLineBase(BaseModel):
    quantity: NonNegativeInt
    subtotal: NonNegativeFloat


class ProductLineCreate(ProductLineBase):
    id_seller_product: int


class ProductLine(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_order: int
    id_seller_product: int
    refund_products: list[RefundProduct] = []


class CompleteProductLine(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_order: int
    id_seller_product: int
    name: str
    description: str
    category: str
    refund_products: list[RefundProduct] = []
