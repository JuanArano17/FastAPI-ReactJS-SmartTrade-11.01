from app.schemas.products.seller_product import SellerProductRead
from pydantic import BaseModel, ConfigDict


class InWishListBase(BaseModel):
    pass


class InWishListCreate(InWishListBase):
    id_seller_product: int


class InWishList(InWishListBase):
    model_config = ConfigDict(from_attributes=True)

    id_buyer: int
    id_seller_product: int


class CompleteWishList(InWishListBase):
    model_config = ConfigDict(from_attributes=True)

    id_buyer: int
    seller_product: SellerProductRead
