from typing import Optional
from fastapi import APIRouter

from app.api.deps import CurrentUserDep, SellerProductServiceDep, ShoppingCartServiceDep
from app.schemas.users.in_shopping_cart import (
    CompleteShoppingCart,
    InShoppingCartCreate,
    InShoppingCartUpdate,
)


cart_token_router = APIRouter(prefix="/shopping_cart/me", tags=["Shopping Carts"])


@cart_token_router.get(
    "/",
    response_model=list[CompleteShoppingCart],
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def read_cart_items(
    *, current_user: CurrentUserDep, shopping_cart_service: ShoppingCartServiceDep
):
    """
    Retrieve cart items from buyer.
    """
    return shopping_cart_service.get_by_user(current_user)


@cart_token_router.post(
    "/",
    response_model=CompleteShoppingCart,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def create_cart_item(
    *,
    current_user: CurrentUserDep,
    shopping_cart_product: InShoppingCartCreate,
    shopping_cart_service: ShoppingCartServiceDep,
    seller_product_service: SellerProductServiceDep,
    id_size: Optional[int] = None
):
    """
    Create a new shopping cart item for the buyer.
    """

    seller_product=seller_product_service.get_by_id(seller_product_id=shopping_cart_product.id_seller_product)
    if seller_product.sizes==[]:
        return shopping_cart_service.add_by_user(current_user, shopping_cart_product)
    else:
         return shopping_cart_service.add_by_user(current_user, shopping_cart_product, id_size)


    


@cart_token_router.delete("/")
async def delete_all_cart_item(
    current_user: CurrentUserDep, shopping_cart_service: ShoppingCartServiceDep
):
    """
    Delete all cart items from a buyer.
    """
    return shopping_cart_service.delete_all_by_user(current_user)


@cart_token_router.put(
    "/{seller_product_id}",
    response_model=CompleteShoppingCart,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def update_quantity(
    *,
    current_user: CurrentUserDep,
    seller_product_id: int,
    cart_item: InShoppingCartUpdate,
    shopping_cart_service: ShoppingCartServiceDep,
):
    """
    Update the quantity of an item in the shopping cart.
    """
    return shopping_cart_service.update_by_user(
        current_user,
        seller_product_id,
        cart_item,
    )


@cart_token_router.delete("/{seller_product_id}")
async def delete_item(
    *,
    current_user: CurrentUserDep,
    seller_product_id: int,
    shopping_cart_service: ShoppingCartServiceDep,
):
    """
    Delete an item from shopping cart.
    """
    return shopping_cart_service.delete_one_by_user(current_user, seller_product_id)
