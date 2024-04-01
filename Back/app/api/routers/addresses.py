from fastapi import APIRouter, HTTPException

from database import get_session
from schemas.address import Address, AddressCreate, AddressUpdate
from service.address import AddressService
from service.buyer import BuyerService
from service.user import UserService

router = APIRouter(prefix="/buyers/{buyer_id}/addresses", tags=["addresses"])

session=get_session()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)
address_service=AddressService(session=session,buyer_service=buyer_service)

@router.get("/", response_model=list[Address])
async def read_addresses(*, buyer_id: int):
    """
    Retrieve addresses from buyer.
    """
    return address_service.get_by_id_buyer(id_buyer=buyer_id)

@router.get("/default", response_model=Address)
async def read_default(*, buyer_id: int):
    """
    Retrieve default address from buyer.
    """
    return address_service.get_default(id_buyer=buyer_id)

@router.post("/", response_model=Address)
async def create_address(*, buyer_id: int ,address: AddressCreate):
    """
    Create a new address for the buyer.
    """
    return address_service.add(id_buyer=buyer_id,address=address)

@router.delete("/")
async def delete_addresses(buyer_id:int):
    """
    Delete all addresses from a buyer.
    """
    return address_service.delete_by_id_buyer(id_buyer=buyer_id)

@router.get("/{address_id}", response_model=Address)
async def read_address(*,buyer_id:int ,address_id: int):
    """
    Retrieve a specific buyer address.
    """

    address=address_service.get_by_id(address_id)
    
    if address is None or address.id_buyer != buyer_id:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address

@router.put("/{address_id}", response_model=Address)
async def update_address(*, buyer_id=int, address_id: int, address: AddressUpdate):
    """
    Update an address.
    """
    existing_address =  address_service.get_by_id(address_id)
    
    if existing_address is None or existing_address.id_buyer != int(buyer_id):
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address_service.update(address_id=address_id,new_data=address)

@router.delete("/{address_id}")
async def delete_address(*, buyer_id=int, address_id: int):
    """
    Delete an address.
    """
    existing_address = address_service.get_by_id(address_id)

    if existing_address is None or existing_address.id_buyer != int(buyer_id):
        raise HTTPException(status_code=404, detail="Address not found")

    return address_service.delete_by_id(address_id)

