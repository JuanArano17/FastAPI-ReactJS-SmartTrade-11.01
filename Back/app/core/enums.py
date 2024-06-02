from enum import Enum


class OrderState(Enum):
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"

class OrderType(Enum):
    STANDARD = "STANDARD"
    PREMIUM= "PREMIUM"