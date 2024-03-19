from Back.app.repositories.buyer import BuyerRepository
from database import get_session


session = get_session()
address_repo = BuyerRepository(session())
address_repo.add(
    "aloecm@gmail.com",
    "Pedrito",
    "Paco",
    0,
    "Pefecwe231",
    "49764160A",
    "Billing address 123",
    "Bizum",
)
