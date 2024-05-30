from typing import Optional
from app.schemas.products.categories.variations.size import Size
from app.schemas.products.seller_product import SellerProductRead
from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.schemas.users.types.buyer import Buyer


class ReviewBase(BaseModel):
    stars: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None,max_length=140)

class ReviewCreate(ReviewBase):
    id_seller_product: int

class ReviewUpdate(ReviewBase):
    comment: str = Field(default=None, max_length=140)
    stars: int = Field(default=None ,ge=1, le=5)


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
    id_seller_product: int


class CompleteReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    id_buyer: int
    stars: int 
    comment: str
    buyer: Buyer
    seller_product: SellerProductRead
