from typing import Optional
from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    url: str


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    url: Optional[str] = None


class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product: int
