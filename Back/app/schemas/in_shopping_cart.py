from pydantic import BaseModel, ConfigDict, PositiveInt


class InShoppingCartBase(BaseModel):
    quantity: PositiveInt


class InShoppingCartCreate(InShoppingCartBase):
    id_seller_product: int


class InShoppingCartUpdate(InShoppingCartBase):
    pass


class InShoppingCart(InShoppingCartBase):
    model_config = ConfigDict(from_attributes=True)

    id_buyer: int
    id_seller_product: int
