from app.service.BuyerService import BuyerService
from database import get_session


session = get_session()
buyer_serv = BuyerService(session())
buyer_serv.add_buyer(
    "aloecm@gmail.com",
    "Pedrito",
    "Paco",
    0,
    "Pefecwe231",
    "49764160A",
    "Billing address 123",
    "Bizum",
)
