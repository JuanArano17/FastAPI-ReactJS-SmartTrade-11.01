from pydantic import BaseModel


class InShoppingCartBase(BaseModel):
    quantity: int


class InShoppingCartCreate(InShoppingCartBase):
    pass


class InShoppingCart(InShoppingCartBase):
    id_buyer: int
    id_product_seller: int

    class Config:
        orm_mode = True
