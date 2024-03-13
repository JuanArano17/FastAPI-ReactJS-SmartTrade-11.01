from pydantic import BaseModel


class InWishListBase(BaseModel):
    pass


class InWishList(InWishListBase):
    id_buyer: int
    id_product_seller: int

    class Config:
        orm_mode = True
