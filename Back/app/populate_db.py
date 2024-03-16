from database import get_session
from repositories.address import AddressRepository

session = get_session()
address_repo = AddressRepository(session())
address_repo.add("Calle Ruzafa", 2, "42", "", "Valencia", "45932", "spain")
