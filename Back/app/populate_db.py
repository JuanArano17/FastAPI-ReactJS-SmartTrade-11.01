from app.service.seller import SellerService
from app.service.buyer import BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_session
from datetime import datetime
#from app.models.buyer import Buyer
#from app.repository import Repository


session = get_session()

category_serv = CategoryService(session)
category_serv.add_category(
    name="games",
    description="cool computer games",
)


        