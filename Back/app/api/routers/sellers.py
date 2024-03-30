from fastapi import APIRouter

from app.schemas.seller import Seller, SellerCreate, SellerUpdate

router = APIRouter()


@router.get("/sellers", response_model=list[Seller])
async def read_sellers():
    """
    Retrieve sellers.
    """


@router.get("/sellers/{seller_id}", response_model=Seller)
async def read_seller(*, seller_id: int):
    """
    Retrieve a seller.
    """


@router.post("/sellers", response_model=Seller)
async def create_seller(*, seller: SellerCreate):
    """
    Create a new seller.
    """


@router.put("/sellers/{seller_id}", response_model=Seller)
async def update_seller(*, seller_id: int, seller: SellerUpdate):
    """
    Update a seller.
    """


@router.delete("/sellers/{seller_id}")
async def delete_seller(*, seller_id: int):
    """
    Delete a seller.
    """


@router.delete("/sellers")
async def delete_sellers():
    """
    Delete all sellers.
    """
