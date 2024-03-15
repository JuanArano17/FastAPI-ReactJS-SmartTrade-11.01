from pydantic import BaseModel, Field


class SellerBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    email: str = Field(
        min_length=1, max_length=320, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )  # EmailStr?
    bank_data: str = Field(min_length=30, max_length=140)
    cif: str = Field(pattern=r"^[A-HJNPQRSUVW]{1}[0-9]{7}[0-9A-J]$")


class SellerCreate(SellerBase):
    password: str
    pass


class Seller(SellerBase):
    id: int
    pass

    class Config:
        orm_mode = True
