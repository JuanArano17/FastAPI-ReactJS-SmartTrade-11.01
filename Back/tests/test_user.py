import unittest
from app.service.user import UserService
from app.service.buyer import BuyerService
from app.database import SessionLocal as get_db
from schemas.buyer import BuyerCreate

session=get_db()
user_service=UserService(session=session)
buyer_service=BuyerService(session=session,user_service=user_service)


class TestUser(unittest.TestCase):
    def test_get_by_email(self):
        buyer_data=BuyerCreate(email="john201@gmail.com", name="John", surname="Webster", eco_points=0,dni="49764160P", billing_address="Main Street", payment_method="Credit Card", password="password")
        buyer=buyer_service.add(buyer_data)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com").id, buyer.id)
        buyer_service.delete_by_id(buyer.id)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com"), None)
    
if __name__ == '__main__':
    unittest.main()