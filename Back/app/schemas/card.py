from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class CardBase(BaseModel):
    card_number: str = Field(min_length=5, max_length=19, pattern=r"^[0-9]+$")
    card_name: str = Field(min_length=1, max_length=60)
    card_exp_date: datetime = Field(gt=date.today)


class CardCreate(CardBase):
    card_security_num: int = Field(min_length=3, max_length=4)


class Card(CardBase):
    id: Optional[int] = None
    # orders: list[Order] = []
    # buyer_owns_cards: list[BuyerOwnsCard] = []

    class Config:
        orm_mode = True
