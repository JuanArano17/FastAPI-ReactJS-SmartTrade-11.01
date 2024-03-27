from pydantic import BaseModel, ConfigDict, NonNegativeFloat, PositiveInt

from app.schemas.refund_product import RefundProduct


class ProductLineBase(BaseModel):
    quantity: PositiveInt
    subtotal: NonNegativeFloat


class ProductLineCreate(ProductLineBase):
    pass


class ProductLine(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_order: int
    id_seller_product: int
    refund_products: list[RefundProduct] = []
