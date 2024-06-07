from typing import Optional
from fastapi import APIRouter

from app.api.deps import CurrentUserDep, SellerProductServiceDep, ReviewServiceDep
from app.schemas.products.review import (
    CompleteReview,
    Review,
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
async def read_reviews(
    *, review_service: ReviewServiceDep, seller_product_id: int
):
    """
    Retrieve seller product reviews.
    """
    return review_service.get_all_by_seller_product(seller_product_id)

@router.get(
    "/can_comment",
    response_model=bool,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def can_comment(
    *, review_service: ReviewServiceDep, seller_product_service: SellerProductServiceDep, seller_product_id: int, current_user: CurrentUserDep
):
    """
    Returns whether or not the user can comment (based on if they already made a review or if they have or have not bought the product).
    """
    seller_product=seller_product_service.get_by_id(seller_product_id)
    
    return (seller_product in review_service.get_seller_product_by_buyer(current_user.id)) and not review_service.review_repo.get_repeat_review(current_user.id, seller_product_id)

@router.post(
    "/",
    response_model=Review,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def post_review(
    *, review_service: ReviewServiceDep, review: ReviewCreate, current_user: CurrentUserDep
):
    """
    Post seller product review.
    """
    return review_service.add(id_buyer=current_user.id, review=review)

router2 = APIRouter(prefix="/reviews", tags=["Reviews"])

@router2.delete(
    "/{review_id}",
    response_model=Review | None,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def delete_cart_items(
    *, review_service: ReviewServiceDep, review_id:int, current_user: CurrentUserDep
):
    """
    Delete cart items.
    """
    return review_service.delete_by_id(id_buyer=current_user.id, id_review=review_id)