from fastapi import APIRouter

from app.schemas.seller import Seller, SellerCreate, SellerUpdate
from database import get_session
from service.seller import SellerService
from service.user import UserService

router = APIRouter(prefix="/sellers", tags=["sellers"])

session=get_session()
user_service=UserService(session=session)
seller_service=SellerService(session=session,user_service=user_service)

@router.get("/", response_model=list[Seller])
async def read_sellers():
    """
    Retrieve sellers.
    """
    return seller_service.get_all()

@router.get("/{seller_id}", response_model=Seller)
async def read_seller(*, seller_id: int):
    """
    Retrieve a seller.
    """
    return seller_service.get_by_id(seller_id)

@router.post("/", response_model=Seller)
async def create_seller(*, seller: SellerCreate):
    """
    Create a new seller.
    """
    return seller.add(seller)


@router.put("/{seller_id}", response_model=Seller)
async def update_seller(*, seller_id: int, seller: SellerUpdate):
    """
    Update a seller.
    """
    return seller_service.update(seller_id,seller)

@router.delete("/{seller_id}")
async def delete_seller(*, seller_id: int):
    """
    Delete a seller.
    """
    return seller_service.delete_by_id(seller_id)


@router.delete("/")
async def delete_sellers():
    """
    Delete all sellers.
    """
    return seller_service.delete_all()
