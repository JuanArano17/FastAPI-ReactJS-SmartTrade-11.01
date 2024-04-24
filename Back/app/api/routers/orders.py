from fastapi import APIRouter

from app.schemas.orders.order import Order, OrderCreate, OrderUpdate, CompleteOrder
from app.api.deps import CurrentUserDep, OrderServiceDep

# router = APIRouter(prefix="/buyers/{buyer_id}/orders", tags=["order"])

orders = APIRouter(prefix="/orders/me", tags=["Order"])


@orders.get("/", response_model=list[CompleteOrder])
async def read_all_current_user_orders(
    current_user: CurrentUserDep, order_service: OrderServiceDep
):
    return order_service.get_all_by_user(current_user)


@orders.get("/{order_id}", response_model=CompleteOrder)
async def read_current_user_order(
    current_user: CurrentUserDep, order_service: OrderServiceDep, order_id: int
):
    return order_service.get_one_by_user(current_user, order_id)


@orders.post("/", response_model=CompleteOrder)
async def create_current_user_order(
    current_user: CurrentUserDep, order_service: OrderServiceDep, order: OrderCreate
):
    return order_service.add(current_user.id, order)


@orders.put("/{order_id}")
async def update_current_user_order(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
    order_id: int,
    order: OrderUpdate,
):
    return order_service.update_by_user(current_user, order_id, order)


@orders.delete("/{order_id}")
async def delete_current_user_order(
    current_user: CurrentUserDep, order_service: OrderServiceDep, order_id: int
):
    order_service.delete_one_by_user(current_user, order_id)


@orders.delete("/")
async def delete_all_current_user_orders(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
):
    order_service.delete_all_by_user(current_user)


# @router.get("/", response_model=list[Order])
# async def read_buyer_orders(buyer_id: int, order_service: OrderServiceDep):
#     """
#     Retrieve orders of a specific buyer.
#     """
#     return order_service.get_all_by_buyer_id(buyer_id)


# @router.get("/{order_id}", response_model=Order)
# async def read_buyer_order(
#     *, buyer_id: int, order_id: int, order_service: OrderServiceDep
# ):
#     """
#     Retrieve an order of a specific buyer.
#     """
#     return order_service.get_buyer_order(buyer_id, order_id)


# @router.post("/", response_model=Order)
# async def create_buyer_order(
#     *, buyer_id: int, order: OrderCreate, order_service: OrderServiceDep
# ):
#     """
#     Create a new order for a specific buyer.
#     """
#     return order_service.add(buyer_id, order)


# @router.put("/{order_id}", response_model=Order)
# async def update_buyer_order(
#     *, buyer_id: int, order_id: int, order: OrderUpdate, order_service: OrderServiceDep
# ):
#     """
#     Update an order of a specific buyer.
#     """
#     return order_service.update(order_id, order)


# @router.delete("/{order_id}")
# async def delete_buyer_order(
#     *, buyer_id: int, order_id: int, order_service: OrderServiceDep
# ):
#     """
#     Delete an order of a specific buyer.
#     """
#     return order_service.delete_by_buyer_id(buyer_id, order_id)


# @router.delete("/")
# async def delete_buyer_orders(buyer_id: int, order_service: OrderServiceDep):
#     """
#     Delete all orders of a specific buyer.
#     """
#     return order_service.delete_all_by_buyer_id(buyer_id)


orders_router = APIRouter(prefix="/orders", tags=["Order"])


@orders_router.get("/", response_model=list[Order])
async def read_orders(order_service: OrderServiceDep):
    """
    Retrieve orders.
    """
    return order_service.get_all()


@orders_router.get("/{order_id}", response_model=CompleteOrder)
async def read_order(*, order_id: int, order_service: OrderServiceDep):
    """
    Retrieve an order.
    """
    return order_service._get_by_id(order_id)


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
