from sqlalchemy.orm import Session
from Back.app.models.seller import Seller
from repository import Repository


class SellerService:
    def __init__(self, session: Session):
        self.session = session
        self.seller_repo = Repository(session, Seller)

    def add_seller(self, email, name, surname, password, cif, bank_data):
        try:
            return self.seller_repo.add(
                email=email,
                name=name,
                surname=surname,
                password=password,
                cif=cif,
                bank_data=bank_data,
            )
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_sellers(self):
        try:
            return self.seller_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_seller(self, pk):
        try:
            return self.seller_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_sellers(self, *expressions):
        try:
            return self.seller_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_seller(self, seller_id, new_data):
        try:
            seller_instance = self.seller_repo.get(seller_id)
            if seller_instance:
                self.seller_repo.update(seller_id, new_data)
                return seller_instance
            else:
                raise ValueError("Seller not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_seller(self, seller_id):
        try:
            seller_instance = self.seller_repo.get(seller_id)
            if seller_instance:
                self.seller_repo.delete(seller_instance)
            else:
                raise ValueError("Seller not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
