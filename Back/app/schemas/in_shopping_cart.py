from pydantic import BaseModel, Field


class InShoppingCartBase(BaseModel):
    quantity: int = Field(ge=0)


class InShoppingCartCreate(InShoppingCartBase):
    pass


class InShoppingCart(InShoppingCartBase):
    id_buyer: int
    id_product_seller: int

    class Config:
        orm_mode = True
