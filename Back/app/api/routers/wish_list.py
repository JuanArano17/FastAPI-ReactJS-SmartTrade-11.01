from fastapi import APIRouter

from app.api.deps import WishListServiceDep
from app.schemas.in_wish_list import InWishList, InWishListCreate

router = APIRouter(prefix="/buyers/{buyer_id}/wish_list", tags=["wish_list"])


@router.get("/", response_model=list[InWishList])
async def read_list_items(*, buyer_id: int, wish_list_service: WishListServiceDep):
    """
    Retrieve list items from buyer.
    """
    wish_list_items = wish_list_service.get_by_id_buyer(id_buyer=buyer_id)
    return wish_list_items


@router.post("/", response_model=InWishList)
async def create_list_item(
    *,
    buyer_id: int,
    wish_list_item: InWishListCreate,
    wish_list_service: WishListServiceDep,
):
    """
    Create a new wish list item for the buyer.
    """
    return wish_list_service.add(id_buyer=buyer_id, wish_list_item=wish_list_item)


@router.delete("/")
async def delete_list(buyer_id: int, wish_list_service: WishListServiceDep):
    """
    Delete all list items from a buyer.
    """
    return wish_list_service.delete_by_id_buyer(id_buyer=buyer_id)


@router.delete("/{seller_product_id}")
async def delete_list_item(
    *, buyer_id=int, seller_product_id: int, wish_list_service: WishListServiceDep
):
    """
    Delete an item from a wish list.
    """
    return wish_list_service.delete_by_id(
        id_buyer=int(buyer_id), id_seller_product=int(seller_product_id)
    )
