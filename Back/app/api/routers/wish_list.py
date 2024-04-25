from fastapi import APIRouter

from app.api.deps import CurrentUserDep, WishListServiceDep
from app.schemas.users.in_wish_list import (
    InWishListCreate,
    CompleteWishList,
)

list_token_router = APIRouter(prefix="/wish_list/me", tags=["Wish Lists"])


@list_token_router.get(
    "/",
    response_model=list[CompleteWishList],
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def read_list_items(
    *, current_user: CurrentUserDep, wish_list_service: WishListServiceDep
):
    """
    Retrieve all wishlist items from the current user.
    """
    return wish_list_service.get_all_by_user(current_user)


@list_token_router.post(
    "/",
    response_model=CompleteWishList,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def create_list_item(
    *,
    current_user: CurrentUserDep,
    wish_list_item: InWishListCreate,
    wish_list_service: WishListServiceDep,
):
    """
    Create a new wishlist item for the current user.
    """
    return wish_list_service.add_by_user(current_user, wish_list_item)


@list_token_router.delete("/")
async def delete_list(
    current_user: CurrentUserDep, wish_list_service: WishListServiceDep
):
    """
    Delete all wishlist items from the current user.
    """
    return wish_list_service.delete_all_by_user(current_user)


@list_token_router.delete("/{seller_product_id}")
async def delete_list_item(
    *,
    current_user: CurrentUserDep,
    seller_product_id: int,
    wish_list_service: WishListServiceDep,
):
    """
    Delete an item from the current user's wish list.
    """
    return wish_list_service.delete_one_by_user(current_user, seller_product_id)
