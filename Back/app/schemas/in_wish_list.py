from pydantic import BaseModel, ConfigDict


class InWishListBase(BaseModel):
    pass


class InWishList(InWishListBase):
    model_config = ConfigDict(from_attributes=True)

    id_buyer: int
    id_seller_product: int
