from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt

from app.schemas.products.categories.variations.size import Size, SizeCreate, SizeUpdate


class ProductState(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"

class SellerProductBase(BaseModel):
    quantity: Optional[NonNegativeInt] = None
    price: NonNegativeFloat
    shipping_costs: NonNegativeFloat
    sizes: Optional[list[SizeCreate]] = []


class SellerProductCreate(SellerProductBase):
    id_product: int

class SellerProductUpdate(SellerProductBase):
    quantity: Optional[NonNegativeInt] = None
    price: Optional[NonNegativeFloat] = None
    shipping_costs: Optional[NonNegativeFloat] = None
    state: Optional[ProductState] = None 
    justification: Optional[str] = Field(default=None, max_length=100)
    eco_points: Optional[NonNegativeFloat] = None
    age_restricted: Optional[bool] = None
    sizes: Optional[list[SizeUpdate]] = []


class SellerProduct(SellerProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product: int
    id_seller: int
    sizes: list[Size] = []
    


class SellerProductRead(BaseModel):
    id: int
    id_product: int
    id_seller: int
    category: str
    state: str
    name: str
    description: Optional[str] = ""
    age_restricted: bool
    eco_points: float
    images: list[str] = []
    price: float
    shipping_costs: float
    spec_sheet: str
    justification: Optional[str] = None
    quantity: int
    stock: int
    author: Optional[str] = None
    pages: Optional[int] = None
    materials: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    capacity: Optional[str] = None
    power_source: Optional[str] = None
    ingredients: Optional[str] = None
    publisher: Optional[str] = None
    platform: Optional[str] = None
    sizes: Optional[list[Size]] = []
    # shopping_cart_products: list[InShoppingCart] = []
    # wish_list_products: list[InWishList] = []
    # product_lines: list[ProductLine] = []
