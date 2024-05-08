from pydantic import BaseModel, ConfigDict
from typing import Optional


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    name: Optional[str]=None


class Country(CountryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CountryList(BaseModel):
    countries: list[str]
