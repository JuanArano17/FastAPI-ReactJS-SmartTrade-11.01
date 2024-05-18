from typing import Optional
from fastapi import APIRouter

from app.api.deps import CurrentUserDep, SellerProductServiceDep, ReviewServiceDep
from app.schemas.products.review import (
    CompleteReview,
    ReviewCreate,
    ReviewUpdate,
)


router = APIRouter(prefix="/seller_products/{seller_product_id}/reviews", tags=["Reviews"])


@router.get(
    "/",
    response_model=list[CompleteReview],
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def read_cart_items(
    *, review_service: ReviewServiceDep, seller_product_id: int
):
    """
    Retrieve cart items from buyer.
    """
    return review_service.get_all_by_seller_product(seller_product_id)