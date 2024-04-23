from typing import Optional
from pydantic import BaseModel, ConfigDict, NonNegativeFloat, NonNegativeInt


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


class SellerProductRead(BaseModel):
    id: int
    id_product: int
    id_seller: int
    category: str
    name: str
    description: Optional[str] = ""
    eco_points: float
    images: list[str] = []
    price: float
    shipping_costs: float
    spec_sheet: str
    quantity: int
    stock: int
    author: Optional[str] = None
    pages: Optional[int] = None
    size: Optional[str] = None
    materials: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    capacity: Optional[str] = None
    power_source: Optional[str] = None
    ingredients: Optional[str] = None
    publisher: Optional[str] = None
    platform: Optional[str] = None
    # shopping_cart_products: list[InShoppingCart] = []
    # wish_list_products: list[InWishList] = []
    # product_lines: list[ProductLine] = []
