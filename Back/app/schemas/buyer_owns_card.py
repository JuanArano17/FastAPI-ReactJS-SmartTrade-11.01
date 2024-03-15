from pydantic import BaseModel


class BuyerOwnsCardBase(BaseModel):
    pass


class BuyerOwnsCardCreate(BuyerOwnsCardBase):
    pass


class BuyerOwnsCard(BuyerOwnsCardBase):
    id_card: int
    id_buyer: int

    class Config:
        orm_mode = True
