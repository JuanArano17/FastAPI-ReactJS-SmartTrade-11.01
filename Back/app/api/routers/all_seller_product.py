from fastapi import APIRouter

from app.api.deps import SellerProductServiceDep
from app.schemas.seller_product import (
    SellerProduct,
)

router = APIRouter(
    prefix="/seller_products", tags=["all-seller-products"]
)


@router.get("/", response_model=list[SellerProduct])
async def read_seller_products(
    *, seller_product_service: SellerProductServiceDep
):
    """
    Retrieve seller products.
    """
    return seller_product_service.get_all()