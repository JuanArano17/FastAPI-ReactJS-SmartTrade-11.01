from Back.app.models.address import Address
from sqlalchemy.orm import Session


def add_address(
    session: Session,
    street,
    floor,
    door,
    adit_info,
    city,
    postal_code,
    country,
    id_buyer,
):
    address = Address(street, floor, door, adit_info, city, postal_code, country)
    #    buyer_address=BuyerAddress(address.id_address,id_buyer)
    session.add(address)
    #    session.add(buyer_address)
    session.commit()


# def assign_address(session, id_address, id_buyer):
#    buyer_address=BuyerAddress(id_address, id_buyer)
#    session.add(buyer_address)
#    session.commit()
