from sqlalchemy import BinaryExpression, select
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

    def get(self, pk):
        try:
            return self.session.get(Address, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Address)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, address_id, new_data):
        try:
            address = self.session.query(Address).filter_by(id=address_id).first()
            if address:
                for key, value in new_data.items():
                    setattr(address, key, value)
                self.session.commit()
            else:
                raise ValueError("Address not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, address_id):
        try:
            address = self.session.query(Address).filter_by(id=address_id).first()
            if address:
                self.session.delete(address)
                self.session.commit()
            else:
                raise ValueError("Address not found.")
        except Exception as e:
            self.session.rollback()
            raise e
