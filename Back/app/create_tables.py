from app.base import Base
from app.database import get_engine
from app.models.buyer import Buyer
from app.models.address import Address
from app.models.product import Product
from app.models.game import Game
from app.models.book import Book
from app.models.clothes import Clothes
from app.models.electronics import Electronics
from app.models.house_utilities import HouseUtilities
from app.models.food import Food
from app.models.electrodomestics import Electrodomestics
from app.models.image import Image
from app.models.card import Card
from app.models.seller import Seller
from app.models.order import Order
from app.models.product_line import ProductLine
from app.models.seller_product import SellerProduct
from app.models.in_shopping_cart import InShoppingCart
from app.models.in_wish_list import InWishList
from app.models.refund_product import RefundProduct

engine = get_engine()
Base.metadata.create_all(bind=engine)

