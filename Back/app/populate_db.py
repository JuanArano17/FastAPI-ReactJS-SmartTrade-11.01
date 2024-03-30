from app.service.seller import SellerService
from app.service.buyer import BuyerRepository, BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_session
from datetime import datetime
from app.service.seller_product import SellerProductService
from schemas.buyer import BuyerCreate, BuyerUpdate
from schemas.product_line import ProductLineCreate
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

session = get_session()

buyer_service=BuyerService(session)
seller_service=SellerService(session)
product_service=ProductService(session)
card_service=CardService(session,buyer_service=buyer_service)
address_service=AddressService(session,buyer_service)
order_service=OrderService(session,buyer_service, card_service,address_service)
seller_product_serv=SellerProductService(session,seller_service=seller_service,product_service=product_service)
product_line_service=ProductLineService(session,buyer_service=buyer_service, order_service=order_service,seller_product_service=seller_product_serv)

buyer=BuyerUpdate(email="seller@gmail.com")
buyer_service.update(1,buyer)
