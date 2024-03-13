from pydantic import BaseModel


class BuyerBase(BaseModel):
    name: str
    surname: str
    email: str
    address: str
    eco_points: float
    dni: str
    billing_address: str
    payment_method: str


class BuyerCreate(BuyerBase):
    password: str
    pass


class Buyer(BuyerBase):
    id: int

    class Config:
        orm_mode = True
