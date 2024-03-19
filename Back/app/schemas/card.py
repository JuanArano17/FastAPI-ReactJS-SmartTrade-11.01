from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date

from Back.app.schemas.buyer_owns_card import BuyerOwnsCard
from Back.app.schemas.order import Order


class CardBase(BaseModel):
    card_number: str = Field(min_length=8, max_length=19, pattern=r"^[0-9]+$")
    card_name: str = Field(min_length=1, max_length=60)
    card_exp_date: datetime = Field(gt=date.today)


class CardCreate(CardBase):
    card_security_num: int = Field(min_length=3, max_length=4)


class Card(CardBase):
    id: Optional[int] = None
    orders: List[Order] = []
    buyer_owns_cards: List[BuyerOwnsCard] = []

    class Config:
        orm_mode = True
