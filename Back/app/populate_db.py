from app.service.seller import SellerService
from app.service.buyer import BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_session
from datetime import datetime
from app.service.seller_product import SellerProductService
from service.image import ImageService
from service.product import ProductService
#from app.models.buyer import Buyer
#from app.repository import Repository


session = get_session()

product_seller_serv = SellerProductService(session)
product_seller_serv.add_seller_product(
    id_product=2,
    id_seller=4,
    quantity=3,
    price=10,
    shipping_costs=3
    )

        