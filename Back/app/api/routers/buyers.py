from fastapi import APIRouter

from app.schemas.buyer import Buyer, BuyerCreate, BuyerUpdate
from database import get_session
from service.buyer import BuyerService
from service.user import UserService

router = APIRouter(prefix="/buyers", tags=["buyers"])

session=get_session()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)


@router.get("/", response_model=list[Buyer])
async def read_buyers():
    """
    Retrieve buyers.
    """
    return buyer_service.get_all()

@router.get("/{buyer_id}", response_model=Buyer)
async def read_buyer(*, buyer_id: int):
    """
    Retrieve a buyer.
    """
    return buyer_service.get_by_id(buyer_id)

@router.post("/", response_model=Buyer)
async def create_buyer(*, buyer: BuyerCreate):
    """
    Create a new buyer.
    """
    return buyer_service.add(buyer)

@router.put("/{buyer_id}", response_model=Buyer)
async def update_buyer(*, buyer_id: int, buyer: BuyerUpdate):
    """
    Update a buyer.
    """
    return buyer_service.update(buyer_id,buyer)

@router.delete("/{buyer_id}")
async def delete_buyer(*, buyer_id: int):
    """
    Delete a buyer.
    """
    return buyer_service.delete_by_id(buyer_id)

@router.delete("/")
async def delete_buyers():
    """
    Delete all buyers.
    """
    return buyer_service.delete_all()


