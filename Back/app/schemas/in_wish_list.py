from pydantic import BaseModel


class InWishListBase(BaseModel):
    pass


class InWishList(InWishListBase):
    id_buyer: int
    id_seller_product: int

    class Config:
        orm_mode = True
