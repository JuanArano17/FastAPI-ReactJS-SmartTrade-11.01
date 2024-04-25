from fastapi import APIRouter

from app.api.deps import BuyerServiceDep
from app.schemas.users.types.buyer import Buyer, BuyerCreate, BuyerUpdate

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.get("/", response_model=list[Buyer])
async def read_buyers(buyer_service: BuyerServiceDep):
    """
    Retrieve buyers.
    """
    return buyer_service.get_all()


@router.get("/{buyer_id}", response_model=Buyer)
async def read_buyer(*, buyer_id: int, buyer_service: BuyerServiceDep):
    """
    Retrieve a buyer.
    """
    return buyer_service.get_by_id(buyer_id)


@router.post("/", response_model=Buyer)
async def create_buyer(*, buyer: BuyerCreate, buyer_service: BuyerServiceDep):
    """
    Create a new buyer.
    """
    return buyer_service.add(buyer)


@router.put("/{buyer_id}", response_model=Buyer)
async def update_buyer(
    *, buyer_id: int, buyer: BuyerUpdate, buyer_service: BuyerServiceDep
):
    """
    Update a buyer.
    """
    return buyer_service.update(buyer_id, buyer)


@router.delete("/{buyer_id}")
async def delete_buyer(*, buyer_id: int, buyer_service: BuyerServiceDep):
    """
    Delete a buyer.
    """
    return buyer_service.delete_by_id(buyer_id)


@router.delete("/")
async def delete_buyers(buyer_service: BuyerServiceDep):
    """
    Delete all buyers.
    """
    return buyer_service.delete_all()
