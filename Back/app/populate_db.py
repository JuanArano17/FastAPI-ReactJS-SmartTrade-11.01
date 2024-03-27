from app.service.seller import SellerService
from app.service.buyer import BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_session
from datetime import datetime
from app.service.seller_product import SellerProductService
from service.image import ImageService
from service.product import ProductService
from service.address import AddressService
from service.in_shopping_cart import InShoppingCartService
from service.in_wish_list import InWishListService
from service.order import OrderService
from service.product_line import ProductLineService


session = get_session()

seller_product_serv = ProductLineService(session)
seller_product_serv.add_product_line(id_order=9, id_seller_product=3, quantity=3)