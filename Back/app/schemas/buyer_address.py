from pydantic import BaseModel


class BuyerAddressBase(BaseModel):
    default: bool


class BuyerAddressCreate(BuyerAddressBase):
    pass


class BuyerAddress(BuyerAddressBase):
    id_buyer: int
    id_address: int

    class Config:
        orm_mode = True
