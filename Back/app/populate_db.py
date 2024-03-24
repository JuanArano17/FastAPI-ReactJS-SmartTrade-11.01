from app.service.SellerService import SellerService
from app.service.BuyerService import BuyerService
from app.service.CardService import CardService
from app.database import get_session
from datetime import datetime
#from app.models.buyer import Buyer
#from app.repository import Repository


session = get_session()

card_serv = CardService(session)
card_serv.add_card(
    id_buyer=1,
    card_number="1234123412341234",
    card_name="Jack Peterson",
    card_security_num=123,
    card_exp_date=datetime(2025,1,1).date(),
)


        