from models.address import Address


class AddressRepository:
    def __init__(self, session):
        self.session = session

    def add(
        self,
        street,
        floor,
        door,
        adit_info,
        city,
        postal_code,
        country,
        default,
        id_buyer,
    ):
        address = Address(
            id_buyer,
            street,
            floor,
            door,
            adit_info,
            city,
            postal_code,
            country,
            default,
        )
        self.session.add(address)
        self.session.commit()
