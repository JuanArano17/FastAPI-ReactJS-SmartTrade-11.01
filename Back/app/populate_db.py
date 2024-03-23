from app.service.BuyerService import BuyerService
from app.database import get_session
#from app.models.buyer import Buyer
#from app.repository import Repository


session = get_session()

#buyer=Buyer(email="jobfgim@gmail.com",
#     name="Fran",
#     surname="Pedro",
#     eco_points=0,
#     password="Pojo231",
#     dni="48764960A",
#     billing_address="Billing address 932",
#     payment_method="Paypal")
#session.add(buyer)
#session.commit()

#repo=Repository(session, Buyer)          
#repo.add(email="jobfgim@gmail.com",
#      name="Fran",
#      surname="Pedro",
#      eco_points=0,
#      password="Pojo231",
#      dni="48764960A",
#      billing_address="Billing address 932",    
#      payment_method="Paypal")

buyer_serv = BuyerService(session)
buyer_serv.add_buyer(
    email="afwcm@gmail.com",
    name="James",
    surname="Francis",
    eco_points=0,
    password="Pefecwe231",
    dni="49765460A",
    billing_address="Billing address 1913",
    payment_method="Bizum")
