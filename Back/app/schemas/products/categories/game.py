from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt

from app.schemas.products.image import Image
from app.schemas.products.seller_product import SellerProduct


class GameBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(min_length=1, max_length=240)
    stock: NonNegativeInt = Field(default=0)
    publisher: str = Field(min_length=1, max_length=40)
    platform: str = Field(min_length=1, max_length=20)
    size: str = Field(max_length=7, pattern=r"^(\d+(\.\d+)?)(\s*[GgMmKk][Bb])?$")


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=40)
    description: Optional[str] = None
    spec_sheet: str = Field(default=None, min_length=1, max_length=240)
    stock: Optional[NonNegativeInt] = None
    publisher: Optional[str] = Field(default=None, min_length=1, max_length=30)
    platform: Optional[str] = Field(default=None, min_length=1, max_length=20)
    size: Optional[str] = Field(
        default=None, max_length=7, pattern=r"^(\d+(\.\d+)?)(\s*[GgMmKk][Bb])?$"
    )


class Game(GameBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    images: List[Image]
    seller_products: List[SellerProduct] = []
