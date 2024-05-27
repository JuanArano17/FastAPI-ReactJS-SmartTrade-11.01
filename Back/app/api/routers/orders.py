from fastapi import APIRouter

from app.schemas.orders.order import (
    CompleteOrder,
    ConfirmOrder,
    OrderUpdate,
)
from app.api.deps import CurrentUserDep, OrderServiceDep

router = APIRouter(prefix="/orders/me", tags=["Orders"])


@router.get("/", response_model=list[CompleteOrder])
async def get_orders(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
):
    """
    Get all orders from the current user.
    """
    return order_service.get_all_by_user(current_user)


@router.post("/", response_model=CompleteOrder, status_code=201)
async def create_order_from_shopping_cart(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
):
    """
    Create an order from the current user's shopping cart.
    """
    order = order_service.create_from_shopping_cart(current_user)
    return order_service._map_order_to_schema(order)


@router.post("/confirm-order", response_model=CompleteOrder, status_code=200)
async def confirm_pending_order(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
    confirm_order: ConfirmOrder,
):
    """
    Confirm the current user's pending order.
    """
    order = order_service.confirm_pending_order(current_user, confirm_order)
    return order_service._map_order_to_schema(order)


@router.get("/{order_id}", response_model=CompleteOrder)
async def get_order(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
    order_id: int,
):
    """
    Get an order by its ID.
    """
    return order_service.get_one_by_user(current_user, order_id)
