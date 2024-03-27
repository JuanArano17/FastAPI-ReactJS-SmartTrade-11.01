from pydantic import BaseModel, ConfigDict, Field, FutureDate
from pydantic_extra_types.payment import PaymentCardNumber


class CardBase(BaseModel):
    card_number: PaymentCardNumber
    card_name: str = Field(min_length=1, max_length=60)
    card_exp_date: FutureDate


class CardCreate(CardBase):
    card_security_num: int = Field(min_length=3, max_length=4)


class Card(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
