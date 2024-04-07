import unittest

from fastapi import HTTPException
from app.service.user import UserService
from app.service.buyer import BuyerService
from app.database import SessionLocal as get_db
from schemas.buyer import BuyerCreate, BuyerUpdate

session=get_db()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)


class TestBuyer(unittest.TestCase):
    def test_add(self):
        buyer_data=BuyerCreate(email="john201@gmail.com", name="John", surname="Webster", eco_points=0,dni="49764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyer=buyer_service.add(buyer_data)
        self.assertEqual(buyer, buyer_service.get_by_id(buyer.id))
        buyer_data=BuyerCreate(email="john201@gmail.com", name="John", surname="Webster", eco_points=0,dni="37764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        self.assertRaises(HTTPException,buyer_service.add,buyer_data)
        buyer_data=BuyerCreate(email="john111@gmail.com", name="John", surname="Webster", eco_points=0,dni="49764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        self.assertRaises(HTTPException,buyer_service.add,buyer_data)
        buyer_service.delete_by_id(buyer.id)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com"), None)
    
    
    def test_get_all(self):
        buyer_data1=BuyerCreate(email="john201@gmail.com", name="John", surname="Webster", eco_points=0,dni="49764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyer_data2=BuyerCreate(email="Mike201@gmail.com", name="Mike", surname="Webster", eco_points=0,dni="37764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyers1=buyer_service.get_all()
        buyer1=buyer_service.add(buyer_data1)
        buyer2=buyer_service.add(buyer_data2)
        buyers2=buyer_service.get_all()
        self.assertEqual(len(buyers1)+2,len(buyers2))
        self.assertIn(buyer1,buyers2)
        self.assertIn(buyer2,buyers2)
        buyer_service.delete_by_id(buyer1.id)
        buyer_service.delete_by_id(buyer2.id)
        buyers=buyer_service.get_all()
        self.assertEqual(buyers,buyers1)
        buyer_service.delete_by_id(buyer1.id)
        buyer_service.delete_by_id(buyer2.id)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com"), None)
        self.assertEqual(user_service.get_by_email(email="Mike201@gmail.com"), None)
    
    
    def test_update(self):
        buyer_data=BuyerCreate(email="john201@gmail.com", name="John", surname="Webster", eco_points=0,dni="49764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyer1=buyer_service.add(buyer_data)
        buyer_data2=BuyerCreate(email="Mike201@gmail.com", name="Mike", surname="Webster", eco_points=0,dni="37764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyer2=buyer_service.add(buyer_data2)
        self.assertEqual(buyer1, buyer_service.get_by_id(buyer1.id))
        self.assertEqual(buyer2, buyer_service.get_by_id(buyer2.id))
        buyer_update1=BuyerUpdate(email="john201@gmail.com")
        buyer_update2=BuyerUpdate(dni="49764160P")
        self.assertRaises(HTTPException,buyer_service.update,buyer1.id,buyer_update1)
        self.assertRaises(HTTPException,buyer_service.update,buyer2.id,buyer_update2)
        buyer_update3=BuyerUpdate(name="Peter",payment_method="Bizum")
        buyer_updated=buyer_service.update(buyer1.id,buyer_update3)
        self.assertEqual(buyer_updated,buyer_service.get_by_id(buyer1.id))
        buyer_update4=BuyerUpdate(payment_method="Credit Card")
        buyer_updated=buyer_service.update(buyer1.id,buyer_update4)
        self.assertEqual(buyer_updated,buyer_service.get_by_id(buyer1.id))
        buyer_update5=BuyerUpdate(name="Frank")
        buyer_updated=buyer_service.update(buyer1.id,buyer_update5)
        self.assertEqual(buyer_updated,buyer_service.get_by_id(buyer1.id))
        buyer_service.delete_by_id(buyer1.id)
        buyer_service.delete_by_id(buyer2.id)
        
        

if __name__ == '__main__':
    unittest.main()