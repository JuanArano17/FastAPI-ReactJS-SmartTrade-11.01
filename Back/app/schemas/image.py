from pydantic import BaseModel


class ImageBase(BaseModel):
    url: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    id_product: int

    class Config:
        orm_mode = True
