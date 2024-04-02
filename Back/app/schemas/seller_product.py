from typing import Optional
from pydantic import BaseModel, ConfigDict, NonNegativeFloat, NonNegativeInt

from app.schemas.product_line import ProductLine
from app.schemas.in_shopping_cart import InShoppingCart
from app.schemas.in_wish_list import InWishList


class SellerProductBase(BaseModel):
    quantity: NonNegativeInt
    price: NonNegativeFloat
    shipping_costs: NonNegativeFloat


class SellerProductCreate(SellerProductBase):
    id_product: int


class SellerProductUpdate(SellerProductBase):
    quantity: Optional[NonNegativeInt] = None
    price: Optional[NonNegativeFloat] = None
    shipping_costs: Optional[NonNegativeFloat] = None


class SellerProduct(SellerProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product: int
    id_seller: int
    shopping_cart_products: list[InShoppingCart] = []
    wish_list_products: list[InWishList] = []
    product_lines: list[ProductLine] = []
