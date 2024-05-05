from typing import Optional
from Back.app.schemas.products.categories.variations.size import Size
from app.schemas.products.seller_product import SellerProductRead
from pydantic import BaseModel, ConfigDict, PositiveInt


class InShoppingCartBase(BaseModel):
    quantity: PositiveInt

class InShoppingCartCreate(InShoppingCartBase):
    id_seller_product: int

class InShoppingCartUpdate(InShoppingCartBase):
    id_size : Optional[int] = None
    quantity: Optional[PositiveInt] = None


class InShoppingCart(InShoppingCartBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
    id_size: Optional[int]=None
    id_seller_product: int


class CompleteShoppingCart(InShoppingCartBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    id_buyer: int
    size: Optional[Size]=None
    seller_product: SellerProductRead
