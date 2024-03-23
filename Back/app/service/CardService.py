from sqlalchemy.orm import Session
from Back.app.models.card import Card
from app.repository import Repository


class CardService:
    def __init__(self, session: Session):
        self.session = session
        self.card_repo = Repository(session, Card)

    def add_card(
        self,
        card_number,
        card_name,
        card_security_num,
        card_exp_date,
        id_buyer,
    ):
        try:
            card = self.card_repo.add(
                card_number=card_number,
                card_name=card_name,
                card_security_num=card_security_num,
                card_exp_date=card_exp_date,
                id_buyer=id_buyer,
            )

            return card
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_card(self, pk):
        try:
            return self.card_repo.get(pk)
        except Exception as e:
            raise e

    def filter_cards(self, *expressions):
        try:
            return self.card_repo.filter(*expressions)
        except Exception as e:
            raise e

    def update_card(self, card_id, new_data):
        try:
            card_instance = self.card_repo.get(card_id)
            if card_instance:
                self.card_repo.update(card_instance, new_data)
                return card_instance
            else:
                raise ValueError("Card not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_cards(self):
        try:
            return self.card_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_card(self, card_id):
        try:
            card_instance = self.card_repo.get(card_id)
            if card_instance:
                self.card_repo.delete(card_instance)
            else:
                raise ValueError("Card not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
