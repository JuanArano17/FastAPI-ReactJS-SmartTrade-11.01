from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional


class AdminBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=20)
    surname: str = Field(min_length=1, max_length=40)


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(AdminBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=40)

class Admin(AdminBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
