from sqlalchemy.orm import Session
from models.buyer import Buyer
from repository import Repository


class BuyerService:
    def __init__(self, session: Session):
        self.session = session
        self.buyer_repo = Repository(session, Buyer)

    def add_buyer(
        self,
        email,
        name,
        surname,
        eco_points,
        password,
        dni,
        billing_address,
        payment_method,
    ):
        try:
            buyer = self.buyer_repo.add(
                email=email,
                name=name,
                surname=surname,
                eco_points=eco_points,
                password=password,
                dni=dni,
                billing_address=billing_address,
                payment_method=payment_method,
            )

            return buyer
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_buyers(self):
        try:
            return self.buyer_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_buyer(self, pk):
        try:
            return self.buyer_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_buyers(self, *expressions):
        try:
            return self.buyer_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_buyer(self, buyer_id, new_data):
        try:
            buyer_instance = self.buyer_repo.get(buyer_id)
            if buyer_instance:
                self.buyer_repo.update(buyer_instance, new_data)
                return buyer_instance
            else:
                raise ValueError("Buyer not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_buyer(self, buyer_id):
        try:
            buyer_instance = self.buyer_repo.get(buyer_id)
            if buyer_instance:
                self.buyer_repo.delete(buyer_instance)
            else:
                raise ValueError("Buyer not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
