from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional

class Order(BaseModel):
  id_order: Optional[int] = None
  id_buyer:int 
  id_card:int
  id_address:int
  order_date:datetime=Field(gt=date(2020,1,1))
  total:float=Field(ge=0)
  #product_lines:list[ProductLine]=[]

  class Config:
        orm_mode = True