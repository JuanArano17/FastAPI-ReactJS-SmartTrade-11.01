from fastapi import APIRouter

from database import get_session
from schemas.in_wish_list import InWishList, InWishListCreate
from service.buyer import BuyerService
from service.in_wish_list import InWishListService
from service.product import ProductService
from service.seller import SellerService
from service.seller_product import SellerProductService
from service.user import UserService

router = APIRouter(prefix="/buyers/{buyer_id}/wish_list", tags=["wish_list"])

session=get_session()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)
seller_service=SellerService(session=session, user_service=user_service)
product_service=ProductService(session=session)
seller_product_service=SellerProductService(session=session,seller_service=seller_service, product_service=product_service)
wish_list_service=InWishListService(session=session,buyer_service=buyer_service, seller_product_service=seller_product_service)

@router.get("/", response_model=list[InWishList])
async def read_list_items(*, buyer_id: int):
    """
    Retrieve list items from buyer.
    """
    wish_list_items=wish_list_service.get_by_id_buyer(id_buyer=buyer_id)
    return wish_list_items
    

@router.post("/", response_model=InWishList)
async def create_list_item(*, buyer_id: int ,wish_list_item: InWishListCreate):
    """
    Create a new wish list item for the buyer.
    """
    return wish_list_service.add(id_buyer=buyer_id,wish_list_item=wish_list_item)

@router.delete("/")
async def delete_list_item(buyer_id:int):
    """
    Delete all list items from a buyer.
    """
    return wish_list_service.delete_by_id_buyer(id_buyer=buyer_id)

@router.delete("/{seller_product_id}")
async def delete_address(*, buyer_id=int, seller_product_id: int):
    """
    Delete an item from wish list.
    """
    return wish_list_service.delete_by_id(id_buyer=int(buyer_id), id_seller_product=int(seller_product_id))
