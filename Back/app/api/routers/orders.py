from app.schemas.order import Order, OrderCreate, OrderUpdate
from fastapi import APIRouter

from app.api.deps import OrderServiceDep

router = APIRouter(prefix="/buyers/{buyer_id}/orders", tags=["order"])


@router.get("/", response_model=list[Order])
async def read_buyer_orders(buyer_id: int, order_service: OrderServiceDep):
    """
    Retrieve orders of a specific buyer.
    """
    return order_service.get_all_by_buyer_id(buyer_id)


@router.get("/{order_id}", response_model=Order)
async def read_buyer_order(
    *, buyer_id: int, order_id: int, order_service: OrderServiceDep
):
    """
    Retrieve an order of a specific buyer.
    """
    return order_service.get_buyer_order(buyer_id, order_id)


@router.post("/", response_model=Order)
async def create_buyer_order(
    *, buyer_id: int, order: OrderCreate, order_service: OrderServiceDep
):
    """
    Create a new order for a specific buyer.
    """
    return order_service.add(buyer_id, order)


@router.put("/{order_id}", response_model=Order)
async def update_buyer_order(
    *, buyer_id: int, order_id: int, order: OrderUpdate, order_service: OrderServiceDep
):
    """
    Update an order of a specific buyer.
    """
    return order_service.update(order_id, order)


@router.delete("/{order_id}")
async def delete_buyer_order(
    *, buyer_id: int, order_id: int, order_service: OrderServiceDep
):
    """
    Delete an order of a specific buyer.
    """
    return order_service.delete_by_buyer_id(buyer_id, order_id)


@router.delete("/")
async def delete_buyer_orders(buyer_id: int, order_service: OrderServiceDep):
    """
    Delete all orders of a specific buyer.
    """
    return order_service.delete_all_by_buyer_id(buyer_id)


orders_router = APIRouter(prefix="/orders", tags=["order"])


@orders_router.get("/", response_model=list[Order])
async def read_orders(order_service: OrderServiceDep):
    """
    Retrieve orders.
    """
    return order_service.get_all()


@orders_router.get("/{order_id}", response_model=Order)
async def read_order(*, order_id: int, order_service: OrderServiceDep):
    """
    Retrieve an order.
    """
    return order_service.get_by_id(order_id)


@orders_router.delete("/{order_id}")
async def delete_order(*, order_id: int, order_service: OrderServiceDep):
    """
    Delete an order.
    """
    return order_service.delete_by_id(order_id)


@orders_router.delete("/")
async def delete_orders(order_service: OrderServiceDep):
    """
    Delete all orders.
    """
    return order_service.delete_all()
