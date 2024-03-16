from typing import Optional
from pydantic import BaseModel, Field


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
    # shopping_cart_products: list[InShoppingCart]=[]
    # wish_list_products: list[InWishList]=[]
    # product_lines: list[ProductLine] = []

    class Config:
        orm_mode = True
