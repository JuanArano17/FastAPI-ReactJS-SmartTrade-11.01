from fastapi import APIRouter

from app.database import get_db
from app.schemas.in_shopping_cart import (
    InShoppingCart,
    InShoppingCartCreate,
    InShoppingCartUpdate,
)
from app.service.buyer import BuyerService
from app.service.in_shopping_cart import InShoppingCartService
from app.service.product import ProductService
from app.service.seller import SellerService
from app.service.seller_product import SellerProductService
from app.service.user import UserService

router = APIRouter(prefix="/buyers/{buyer_id}/shopping_cart", tags=["shopping_cart"])

session = get_db()
user_service = UserService(session=session)
buyer_service = BuyerService(session=session, user_service=user_service)
seller_service = SellerService(session=session, user_service=user_service)
product_service = ProductService(session=session)
seller_product_service = SellerProductService(
    session=session, seller_service=seller_service, product_service=product_service
)
shopping_cart_service = InShoppingCartService(
    session=session,
    buyer_service=buyer_service,
    seller_product_service=seller_product_service,
)


@router.get("/", response_model=list[InShoppingCart])
async def read_cart_items(*, buyer_id: int):
    """
    Retrieve cart items from buyer.
    """
    shopping_cart_items = shopping_cart_service.get_by_id_buyer(id_buyer=buyer_id)
    # seller_products=[]
    # for item in shopping_cart_items:
    #    seller_products.append(seller_product_service.get_by_id(item.id_seller_product))

    # TODO: MAKE SURE THAT THE SELLER PRODUCTS APPEND THE ITEMS TO THEIR LISTS
    return shopping_cart_items


@router.post("/", response_model=InShoppingCart)
async def create_cart_item(
    *, buyer_id: int, shopping_cart_product: InShoppingCartCreate
):
    """
    Create a new shopping cart item for the buyer.
    """
    return shopping_cart_service.add(
        id_buyer=buyer_id, shopping_cart_product=shopping_cart_product
    )


@router.delete("/")
async def delete_cart_item(buyer_id: int):
    """
    Delete all cart items from a buyer.
    """
    return shopping_cart_service.delete_by_id_buyer(id_buyer=buyer_id)


@router.put("/{seller_product_id}", response_model=InShoppingCart)
async def update_quantity(
    *, buyer_id=int, seller_product_id: int, cart_item: InShoppingCartUpdate
):
    """
    Update the quantity of an item in the shopping cart.
    """
    return shopping_cart_service.update(
        id_buyer=int(buyer_id),
        id_seller_product=int(seller_product_id),
        new_data=cart_item,
    )


@router.delete("/{seller_product_id}")
async def delete_item(*, buyer_id=int, seller_product_id: int):
    """
    Delete an item from shopping cart.
    """
    return shopping_cart_service.delete_by_id(
        id_buyer=int(buyer_id), id_seller_product=int(seller_product_id)
    )
