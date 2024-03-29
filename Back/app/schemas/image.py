from typing import Optional
from pydantic import AnyUrl, BaseModel, ConfigDict


class ImageBase(BaseModel):
    url: AnyUrl


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    url: Optional[AnyUrl] = None


class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_product: int
