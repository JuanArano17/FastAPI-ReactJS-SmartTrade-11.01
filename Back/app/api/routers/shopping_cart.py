from fastapi import APIRouter

from app.api.deps import CurrentUserDep, ShoppingCartServiceDep
from app.schemas.in_shopping_cart import (
    InShoppingCart,
    InShoppingCartCreate,
    InShoppingCartUpdate,
)


cart_token_router = APIRouter(prefix="/shopping_cart/me", tags=["shopping_cart_with_token"])

@cart_token_router.get("/", response_model=list[InShoppingCart])
async def read_cart_items(
    *, user_dep: CurrentUserDep, shopping_cart_service: ShoppingCartServiceDep
):
    """
    Retrieve cart items from buyer.
    """
    shopping_cart_items = shopping_cart_service.get_by_id_buyer(id_buyer=user_dep.id)
    # seller_products=[]
    # for item in shopping_cart_items:
    #    seller_products.append(seller_product_service.get_by_id(item.id_seller_product))

    # TODO: MAKE SURE THAT THE SELLER PRODUCTS APPEND THE ITEMS TO THEIR LISTS
    return shopping_cart_items


@cart_token_router.post("/", response_model=InShoppingCart)
async def create_cart_item(
    *,
    user_dep: CurrentUserDep,
    shopping_cart_product: InShoppingCartCreate,
    shopping_cart_service: ShoppingCartServiceDep,
):
    """
    Create a new shopping cart item for the buyer.
    """
    return shopping_cart_service.add(
        id_buyer=user_dep.id, shopping_cart_product=shopping_cart_product
    )


@cart_token_router.delete("/")
async def delete_cart_item(
    user_dep: CurrentUserDep, shopping_cart_service: ShoppingCartServiceDep
):
    """
    Delete all cart items from a buyer.
    """
    return shopping_cart_service.delete_by_id_buyer(id_buyer=user_dep.id)


@cart_token_router.put("/{seller_product_id}", response_model=InShoppingCart)
async def update_quantity(
    *,
    user_dep: CurrentUserDep,
    seller_product_id: int,
    cart_item: InShoppingCartUpdate,
    shopping_cart_service: ShoppingCartServiceDep,
):
    """
    Update the quantity of an item in the shopping cart.
    """
    return shopping_cart_service.update(
        id_buyer=int(user_dep.id),
        id_seller_product=int(seller_product_id),
        new_data=cart_item,
    )


@cart_token_router.delete("/{seller_product_id}")
async def delete_item(
    *,
    user_dep: CurrentUserDep,
    seller_product_id: int,
    shopping_cart_service: ShoppingCartServiceDep,
):
    """
    Delete an item from shopping cart.
    """
    return shopping_cart_service.delete_by_id(
        id_buyer=int(user_dep.id), id_seller_product=int(seller_product_id)
    )