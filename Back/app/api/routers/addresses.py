from fastapi import APIRouter

from database import get_session
from schemas.address import Address, AddressCreate, AddressUpdate
from service.address import AddressService
from service.buyer import BuyerService
from service.user import UserService

router = APIRouter(tags=["addresses"])

session=get_session()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)
address_service=AddressService(session=session,buyer_service=buyer_service)

@router.get("/buyers/{buyer_id}/addresses/", response_model=list[Address])
async def read_addresses(*, buyer_id: int):
    """
    Retrieve addresses from buyer.
    """
    return address_service.get_by_id_buyer(id_buyer=buyer_id)

@router.get("/buyers/{buyer_id}/addresses/default", response_model=Address)
async def read_default(*, buyer_id: int):
    """
    Retrieve default address from buyer.
    """
    return address_service.get_default(id_buyer=buyer_id)

@router.post("/buyers/{buyer_id}/addresses/", response_model=Address)
async def create_address(*, buyer_id: int ,address: AddressCreate):
    """
    Create a new address for the buyer.
    """
    return address_service.add(id_buyer=buyer_id,address=address)

@router.delete("/buyers/{buyer_id}/addresses/")
async def delete_addresses():
    """
    Delete all addresses from a buyer.
    """
    return address_service.delete_all()



@router.get("/addresses/{address_id}", response_model=Address)
async def read_address(*,address_id: int):
    """
    Retrieve a specific address.
    """
    return address_service.get_by_id(address_id)

@router.put("/addresses/{address_id}", response_model=Address)
async def update_address(*, address_id: int, address: AddressUpdate):
    """
    Update an address.
    """
    return address_service.update(address_id,address)

@router.delete("addresses/{address_id}")
async def delete_address(*, address_id: int):
    """
    Delete an address.
    """
    return address_service.delete_by_id(address_id)

