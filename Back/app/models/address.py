from pydantic import BaseModel, Field
from typing import Optional
from Back.app.database import Order

class Address(BaseModel):
  id_address: Optional[int] = None
  street:str = Field(min_length=5, max_length=35)
  floor:Optional[int] =Field(ge=0, le=200)
  door:str =Field(min_length=1, max_length=6)
  adit_info: Optional[str]=Field(max_length=70)
  city: str=Field(min_length=1, max_length=28)
  postal_code: str=Field(min_length=5, max_length=8) 
  country: str=Field(min_length=4,max_length=28)
  orders: list[Order]=[]
  #buyer_addresses: list[BuyerAddress]=[]

  class Config:
    orm_mode=True