from fastapi import APIRouter

from app.api.deps import CurrentUserDep, WishListServiceDep
from app.schemas.users.in_wish_list import InWishList, InWishListCreate

list_token_router = APIRouter(prefix="/wish_list/me", tags=["Wish Lists"])


@list_token_router.get("/", response_model=list[InWishList])
async def read_list_items(
    *, user_dep: CurrentUserDep, wish_list_service: WishListServiceDep
):
    """
    Retrieve list items from buyer.
    """
    wish_list_items = wish_list_service.get_by_id_buyer(id_buyer=user_dep.id)
    return wish_list_items


@list_token_router.post("/", response_model=InWishList)
async def create_list_item(
    *,
    user_dep: CurrentUserDep,
    wish_list_item: InWishListCreate,
    wish_list_service: WishListServiceDep,
):
    """
    Create a new wish list item for the buyer.
    """
    return wish_list_service.add(id_buyer=user_dep.id, wish_list_item=wish_list_item)


@list_token_router.delete("/")
async def delete_list(wish_list_service: WishListServiceDep, user_dep: CurrentUserDep):
    """
    Delete all list items from a buyer.
    """
    return wish_list_service.delete_by_id_buyer(id_buyer=user_dep)


@list_token_router.delete("/{seller_product_id}")
async def delete_list_item(
    *,
    seller_product_id: int,
    wish_list_service: WishListServiceDep,
    user_dep: CurrentUserDep,
):
    """
    Delete an item from a wish list.
    """
    return wish_list_service.delete_by_id(
        id_buyer=int(user_dep.id), id_seller_product=int(seller_product_id)
    )
