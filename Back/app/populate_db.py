from database import get_session
from repositories.address import AddressRepository

# might need to create constructors cause it's making me use the id
# add auto_increments
session = get_session()
address_repo = AddressRepository(session)
address_repo.add("Calle paco", 1, "322", "Hello there", "Valencia", "45332", "spain")
