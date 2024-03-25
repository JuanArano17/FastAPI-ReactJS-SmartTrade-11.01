from sqlalchemy.orm import Session
from app.models.card import Card
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
            # Check if a card with the same buyer id and card number already exists
            existing_card = self.filter_cards(
                Card.id_buyer == id_buyer,
                Card.card_number == card_number
            )

            if existing_card:
                raise ValueError("Card with the same buyer id and card number already exists.")
            
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
            id_buyer = new_data.get('id_buyer')
            card_number = new_data.get('card_number')
            if(card_number==None):
                card_number=card_instance.card_number
            if(id_buyer==None):
                id_buyer=card_instance.id_buyer
            existing_card = self.card_repo.filter(
                Card.id != card_id,  # Exclude the current card being updated
                Card.id_buyer == id_buyer,
                Card.card_number == card_number
            )

            if len(existing_card)>0:
                raise ValueError("Card with the same buyer id and card number already exists.")

            
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
