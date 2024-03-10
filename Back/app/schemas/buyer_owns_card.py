from pydantic import BaseModel, Field

class BuyerOwnsCard(BaseModel):
  id_card:int
  id_buyer:int 
  
  class Config:
        orm_mode = True
  