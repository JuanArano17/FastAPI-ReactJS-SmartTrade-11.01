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
#from app.models.buyer import Buyer
#from app.repository import Repository


session = get_session()

card_serv = CardService(session)
card_serv.update_card(1, {"card_number":"1234123412341234"})

         