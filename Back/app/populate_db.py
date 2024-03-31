from pydantic_extra_types.payment import PaymentCardNumber
from app.service.seller import SellerService
from app.service.buyer import BuyerRepository, BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_session
from datetime import datetime
from app.service.seller_product import SellerProductService
from schemas.buyer import BuyerCreate, BuyerUpdate
from schemas.card import CardCreate, CardUpdate
from schemas.category import CategoryCreate, CategoryUpdate
from schemas.in_shopping_cart import InShoppingCartCreate, InShoppingCartUpdate
from schemas.in_wish_list import InWishListCreate
from schemas.product import ProductCreate, ProductCreateWithCategory
from schemas.product_line import ProductLineCreate
from schemas.seller_product import SellerProductCreate, SellerProductUpdate
from service.image import ImageService
from service.product import ProductService
from service.address import AddressService
from service.in_shopping_cart import InShoppingCartService
from service.in_wish_list import InWishListService
from service.order import OrderService
from service.product_line import ProductLineService
from service.refund_product import RefundProductService
from schemas.refund_product import RefundProductCreate
from schemas.order import OrderCreate
from service.user import UserService

session = get_session()
user_service=UserService(session=session)
buyer_service=BuyerService(session, user_service=user_service)
seller_service=SellerService(session, user_service=user_service)
category_service=CategoryService(session)
product_service=ProductService(session)
image_service=ImageService(session, product_service)
card_service=CardService(session,buyer_service=buyer_service)
address_service=AddressService(session,buyer_service)
order_service=OrderService(session,buyer_service, card_service,address_service)
seller_product_serv=SellerProductService(session,seller_service=seller_service,product_service=product_service)
in_shopping_cart_service=InShoppingCartService(session,buyer_service,seller_product_serv)
in_wish_list_service=InWishListService(session=session,buyer_service=buyer_service,seller_product_service=seller_product_serv)
product_line_service=ProductLineService(session,buyer_service=buyer_service, order_service=order_service,seller_product_service=seller_product_serv)
refund_product_service=RefundProductService(session=session,buyer_service=buyer_service, order_service=order_service,seller_product_service=seller_product_serv,product_line_service=product_line_service)

refund_product=RefundProductCreate(quantity=2, refund_date=datetime(2021,1,2).date())
refund_product_service.delete_by_id(id_order=3,id_buyer=1, id_product_line=4,refund_product_id=8)

