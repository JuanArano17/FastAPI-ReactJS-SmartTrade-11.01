from pydantic import BaseModel


class InWishListBase(BaseModel):
    pass


class InWishList(InWishListBase):
    id_buyer: str
    id_product: int

    class Config:
        orm_mode = True
