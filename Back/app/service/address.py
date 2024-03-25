from sqlalchemy.orm import Session
from app.models.address import Address
from app.repository import Repository


class AddressService:
    def __init__(self, session: Session):
        self.session = session
        self.address_repo = Repository(session, Address)

    def add_address(
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
            if default:
                # Check if there's already a default address for the buyer
                existing_default = self.address_repo.filter(
                    Address.default, Address.id_buyer == id_buyer
                )

                if len(existing_default)>0:
                    # If default address exists, update it to not be default
                    self.update_address(existing_default[0].id, {"default": False})

            address = self.address_repo.add(
                street=street,
                floor=floor,
                door=door,
                adit_info=adit_info,
                city=city,
                postal_code=postal_code,
                country=country,
                default=default,
                id_buyer=id_buyer,
            )

            return address
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_addresses(self):
        try:
            return self.address_repo.list()
        except Exception as e:
            raise e

    def get_address(self, pk):
        try:
            return self.address_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_addresses(self, *expressions):
        try:
            return self.address_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_address(self, address_id, new_data):
        try:
            address = self.address_repo.get(address_id)
            if address is None:
                raise ValueError("Address not found.")

            if "default" in new_data and new_data["default"]:
                # Check if there's already a default address for the buyer
                existing_default = self.address_repo.filter(
                    Address.default, Address.id_buyer == address.id_buyer
                )
                if existing_default:
                    # If default address exists, update it to not be default
                    self.address_repo.update(existing_default[0], {"default": False})

            self.address_repo.update(address, new_data)
            return address
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_address(self, address_id):
        try:
            address_instance = self.address_repo.get(address_id)
            if address_instance:
                self.address_repo.delete(address_instance)
            else:
                raise ValueError("Address not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
