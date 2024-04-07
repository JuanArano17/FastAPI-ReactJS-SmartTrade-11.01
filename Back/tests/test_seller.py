import unittest

from fastapi import HTTPException
from app.service.user import UserService
from app.service.seller import SellerService
from app.database import SessionLocal as get_db
from schemas.seller import SellerUpdate, SellerCreate, SellerUpdate


session=get_db()
user_service=UserService(session=session)
seller_service=SellerService(session=session,user_service=user_service)


class TestSeller(unittest.TestCase):
    
    def test_add(self):
        seller_data=SellerCreate(email="john201@gmail.com", name="John", surname="Webster", bank_data="GB40FFXQ16064040004057",cif="G49764260", password="password")
        seller=seller_service.add(seller_data)
        self.assertEqual(seller, seller_service.get_by_id(seller.id))
        seller_data=SellerCreate(email="john201@gmail.com", name="John", surname="Webster", bank_data="GB41111Q19964040004099",cif="X38564260", password="password")
        self.assertRaises(HTTPException,seller_service.add,seller_data)
        seller_data=SellerCreate(email="john111@gmail.com", name="John", surname="Webster", bank_data="GB41111Q19964040004099",cif="G49764260", password="password")
        self.assertRaises(HTTPException,seller_service.add,seller_data)
        seller_service.delete_by_id(seller.id)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com"), None)
    
    
    def test_get_all(self):
        seller_data1=SellerCreate(email="john201@gmail.com", name="John", surname="Webster", bank_data="GB41111Q19964040004099",cif="X38564260", password="password")
        seller_data2=SellerCreate(email="Mike201@gmail.com", name="Mike", surname="Webster", bank_data="GB40FFXQ16064040004057",cif="G49764260", password="password")
        sellers1=seller_service.get_all()
        seller1=seller_service.add(seller_data1)
        seller2=seller_service.add(seller_data2)
        sellers2=seller_service.get_all()
        self.assertEqual(len(sellers1)+2,len(sellers2))
        self.assertIn(seller1,sellers2)
        self.assertIn(seller2,sellers2)
        seller_service.delete_by_id(seller1.id)
        seller_service.delete_by_id(seller2.id)
        sellers=seller_service.get_all()
        self.assertEqual(sellers,sellers1)
        seller_service.delete_by_id(seller1.id)
        seller_service.delete_by_id(seller2.id)
        self.assertEqual(user_service.get_by_email(email="john201@gmail.com"), None)
        self.assertEqual(user_service.get_by_email(email="Mike201@gmail.com"), None)
    
    
    def test_update(self):
        seller_data=SellerCreate(email="john201@gmail.com", name="John", surname="Webster", bank_data="GB41111Q19964040004099",cif="X38564260", password="password")
        seller1=seller_service.add(seller_data)
        seller_data2=SellerCreate(email="Mike201@gmail.com", name="Mike", surname="Webster", bank_data="GB40FFXQ16064040004057",cif="G49764260", password="password")
        seller2=seller_service.add(seller_data2)
        self.assertEqual(seller1, seller_service.get_by_id(seller1.id))
        self.assertEqual(seller2, seller_service.get_by_id(seller2.id))
        seller_update1=SellerUpdate(email="john201@gmail.com")
        seller_update2=SellerUpdate(cif="X38564260")
        self.assertRaises(HTTPException,seller_service.update,seller1.id,seller_update1)
        self.assertRaises(HTTPException,seller_service.update,seller2.id,seller_update2)
        seller_update3=SellerUpdate(name="Peter",bank_data="GB411111111111111111111")
        seller_updated=seller_service.update(seller1.id,seller_update3)
        self.assertEqual(seller_updated,seller_service.get_by_id(seller1.id))
        seller_update4=SellerUpdate(bank_data="GB400001111111111110000")
        seller_updated=seller_service.update(seller1.id,seller_update4)
        self.assertEqual(seller_updated,seller_service.get_by_id(seller1.id))
        seller_update5=SellerUpdate(name="Frank")
        seller_updated=seller_service.update(seller1.id,seller_update5)
        self.assertEqual(seller_updated,seller_service.get_by_id(seller1.id))
        seller_service.delete_by_id(seller1.id)
        seller_service.delete_by_id(seller2.id)
        
if __name__ == '__main__':
    unittest.main()