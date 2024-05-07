from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt



class SizeBase(BaseModel):
    size: str
    quantity: NonNegativeInt

class SizeCreate(SizeBase):
    pass

class SizeUpdate(SizeBase):
    size: Optional[str]
    quantity: Optional[NonNegativeInt]


class Size(SizeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seller_product_id: int