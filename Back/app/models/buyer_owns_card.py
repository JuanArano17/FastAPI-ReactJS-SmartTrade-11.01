from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional

class BuyerOwnsCard(BaseModel):
  id_card:int
  id_buyer:int 
  
  class Config:
        orm_mode = True
  