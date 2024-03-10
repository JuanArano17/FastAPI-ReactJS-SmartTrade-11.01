from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RefundProduct(BaseModel):
  id_refund_product: Optional[int] = None
  id_product_line: int
  quantity:int=Field(gt=0) 
  refund_date:datetime
  
  class Config:
    orm_mode=True