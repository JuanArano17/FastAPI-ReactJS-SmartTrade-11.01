from pydantic import BaseModel


class InShoppingCartBase(BaseModel):
    quantity: int


class InShoppingCartCreate(InShoppingCartBase):
    pass


class InShoppingCart(InShoppingCartBase):
    id_buyer: str
    id_product: int

    class Config:
        orm_mode = True
