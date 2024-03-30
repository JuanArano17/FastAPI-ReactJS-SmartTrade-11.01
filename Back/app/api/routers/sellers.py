from fastapi import APIRouter

from app.schemas.seller import Seller, SellerCreate, SellerUpdate

router = APIRouter(prefix="/sellers", tags=["sellers"])


@router.get("/", response_model=list[Seller])
async def read_sellers():
    """
    Retrieve sellers.
    """


@router.get("/{seller_id}", response_model=Seller)
async def read_seller(*, seller_id: int):
    """
    Retrieve a seller.
    """


@router.post("/", response_model=Seller)
async def create_seller(*, seller: SellerCreate):
    """
    Create a new seller.
    """


@router.put("/{seller_id}", response_model=Seller)
async def update_seller(*, seller_id: int, seller: SellerUpdate):
    """
    Update a seller.
    """


@router.delete("/{seller_id}")
async def delete_seller(*, seller_id: int):
    """
    Delete a seller.
    """


@router.delete("/")
async def delete_sellers():
    """
    Delete all sellers.
    """
