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
        try:
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
            # if default, set other address to not default, if such address exists
            self.session.add(address)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            addresses = self.session.query(Address).all()
            return addresses
        except Exception as e:
            raise e
