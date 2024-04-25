from fastapi import APIRouter, HTTPException

from app.api.deps import SellerProductServiceDep
from app.schemas.products.seller_product import (
    SellerProductRead
)

router = APIRouter(prefix="/admin", tags=["seller-products"])


@router.get(
    "/seller-products", response_model=list[SellerProductRead], response_model_exclude_none=True
)
async def read_seller_products_pure(*, seller_product_service: SellerProductServiceDep):
    """
    Retrieve seller products.
    """
    return seller_product_service.get_all_by_state("Pending")