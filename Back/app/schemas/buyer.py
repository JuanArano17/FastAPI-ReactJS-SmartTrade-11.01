from pydantic import BaseModel, Field


class BuyerBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)
    email: str = Field(
        min_length=1, max_length=320, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )  # EmailStr?
    eco_points: float = Field(ge=0)
    dni: str = Field(min_length=9, max_length=9, pattern=r"^\d{8}[a-zA-Z]$")
    billing_address: str = Field(min_length=1, max_length=100)
    payment_method: str = Field(min_length=1, max_length=20)


class BuyerCreate(BuyerBase):
    password: str
    pass


class Buyer(BuyerBase):
    id: int

    class Config:
        orm_mode = True
