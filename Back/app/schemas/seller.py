from pydantic import BaseModel


class SellerBase(BaseModel):
    name: str
    surname: str
    email: str
    bank_data: str
    cif: str


class SellerCreate(SellerBase):
    password: str
    pass


class Seller(SellerBase):
    id: int
    pass

    class Config:
        orm_mode = True
