from typing import Optional
from pydantic import BaseModel, Field

from Back.app.models.product_line import ProductLine
from Back.app.schemas.in_shopping_cart import InShoppingCart
from Back.app.schemas.in_wish_list import InWishList


class SellerProductBase(BaseModel):
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)
    shipping_costs: float = Field(ge=0)


class SellerProductCreate(SellerProductBase):
    pass


class SellerProduct(SellerProductBase):
    id: Optional[int] = None
    id_product: int
    id_seller: int
    shopping_cart_products: list[InShoppingCart] = []
    wish_list_products: list[InWishList] = []
    product_lines: list[ProductLine] = []

    class Config:
        orm_mode = True
