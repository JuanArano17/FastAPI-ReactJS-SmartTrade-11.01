from pydantic import BaseModel, ConfigDict, NonNegativeFloat, PositiveInt

from app.models.product_line import ProductLine
from app.schemas.in_shopping_cart import InShoppingCart
from app.schemas.in_wish_list import InWishList


class SellerProductBase(BaseModel):
    quantity: PositiveInt
    price: NonNegativeFloat
    shipping_costs: NonNegativeFloat


class SellerProductCreate(SellerProductBase):
    pass


class SellerProduct(SellerProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product: int
    id_seller: int
    shopping_cart_products: list[InShoppingCart] = []
    wish_list_products: list[InWishList] = []
    product_lines: list[ProductLine] = []
