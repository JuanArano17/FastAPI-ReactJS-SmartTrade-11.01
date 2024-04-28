from fastapi import APIRouter

from app.api.deps import AddressServiceDep, CurrentUserDep
from app.schemas.users.address import Address, AddressCreate, AddressUpdate

# router = APIRouter(prefix="/buyers/{buyer_id}/addresses", tags=["Addresses"])

address_router = APIRouter(prefix="/addresses", tags=["Addresses"])


@address_router.get("/", response_model=list[Address])
async def read_my_addresses(
    *, current_user: CurrentUserDep, address_service: AddressServiceDep
):
    """
    Retrieve all current user's addresses.
    """
    return address_service.get_all_by_user(current_user)


@address_router.get("/default", response_model=Address)
async def read_my_default_address(
    *, current_user: CurrentUserDep, address_service: AddressServiceDep
):
    """
    Retrieve current user's default address.
    """
    return address_service.get_default_by_user(current_user)


@address_router.get("/{address_id}", response_model=Address)
async def read_my_address(
    *, address_id: int, current_user: CurrentUserDep, address_service: AddressServiceDep
):
    """
    Retrieve a specific address from the current user.
    """
    return address_service.get_one_by_user(current_user, address_id)


@address_router.post("/", response_model=Address)
async def create_my_address(
    *,
    address: AddressCreate,
    current_user: CurrentUserDep,
    address_service: AddressServiceDep,
):
    """
    Create a new address for the current user.
    """
    return address_service.add_by_user(current_user, address)


@address_router.put("/{address_id}", response_model=Address)
async def update_my_address(
    *,
    address_id: int,
    address: AddressUpdate,
    current_user: CurrentUserDep,
    address_service: AddressServiceDep,
):
    """
    Update an address from the current user.
    """
    return address_service.update_by_user(current_user, address_id, address)


@address_router.delete("/")
async def delete_my_addresses(
    *, current_user: CurrentUserDep, address_service: AddressServiceDep
):
    """
    Delete all addresses from the current user.
    """
    return address_service.delete_all_by_user(current_user)


@address_router.delete("/{address_id}")
async def delete_my_address(
    *, address_id: int, current_user: CurrentUserDep, address_service: AddressServiceDep
):
    """
    Delete an address from the current user.
    """
    return address_service.delete_one_by_user(current_user, address_id)


# @router.get("/", response_model=list[Address])
# async def read_addresses(*, buyer_id: int, address_service: AddressServiceDep):
#     """
#     Retrieve addresses from buyer.
#     """
#     return address_service.get_by_id_buyer(id_buyer=buyer_id)


# @router.get("/default", response_model=Address)
# async def read_default(*, buyer_id: int, address_service: AddressServiceDep):
#     """
#     Retrieve default address from buyer.
#     """
#     return address_service.get_default(id_buyer=buyer_id)


# @router.post("/", response_model=Address)
# async def create_address(
#     *, buyer_id: int, address: AddressCreate, address_service: AddressServiceDep
# ):
#     """
#     Create a new address for the buyer.
#     """
#     return address_service.add(id_buyer=buyer_id, address=address)


# @router.delete("/")
# async def delete_addresses(buyer_id: int, address_service: AddressServiceDep):
#     """
#     Delete all addresses from a buyer.
#     """
#     return address_service.delete_by_id_buyer(id_buyer=buyer_id)


# @router.get("/{address_id}", response_model=Address)
# async def read_address(
#     *, buyer_id: int, address_id: int, address_service: AddressServiceDep
# ):
#     """
#     Retrieve a specific buyer address.
#     """

#     address = address_service.get_by_id(address_id)

#     if address is None or address.id_buyer != buyer_id:
#         raise HTTPException(status_code=404, detail="Address not found")

#     return address


# @router.put("/{address_id}", response_model=Address)
# async def update_address(
#     *,
#     buyer_id=int,
#     address_id: int,
#     address: AddressUpdate,
#     address_service: AddressServiceDep,
# ):
#     """
#     Update an address.
#     """
#     existing_address = address_service.get_by_id(address_id)

#     if existing_address is None or existing_address.id_buyer != int(buyer_id):
#         raise HTTPException(status_code=404, detail="Address not found")

#     return address_service.update(address_id=address_id, new_data=address)


# @router.delete("/{address_id}")
# async def delete_address(
#     *, buyer_id=int, address_id: int, address_service: AddressServiceDep
# ):
#     """
#     Delete an address.
#     """
#     existing_address = address_service.get_by_id(address_id)

#     if existing_address is None or existing_address.id_buyer != int(buyer_id):
#         raise HTTPException(status_code=404, detail="Address not found")

#     return address_service.delete_by_id(address_id)
