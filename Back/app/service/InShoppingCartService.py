from sqlalchemy.orm import Session
from Back.app.models.in_shopping_cart import InShoppingCart
from app.repository import Repository


class InShoppingCartService:
    def __init__(self, session: Session):
        self.session = session
        self.cart_repo = Repository(session, InShoppingCart)

    def add_to_cart(self, id_seller_product, id_buyer, quantity):
        try:
            return self.cart_repo.add(
                id_seller_product=id_seller_product,
                id_buyer=id_buyer,
                quantity=quantity,
            )
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_cart_items(self):
        try:
            return self.cart_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_cart_item(self, cart_item_id):
        try:
            return self.cart_repo.get(cart_item_id)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_cart_items(self, *expressions):
        try:
            return self.cart_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_cart_item(self, cart_item_id, new_data):
        try:
            cart_item_instance = self.cart_repo.get(cart_item_id)
            if cart_item_instance:
                self.cart_repo.update(cart_item_instance, new_data)
                return cart_item_instance
            else:
                raise ValueError("Cart item not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_cart_item(self, cart_item_id):
        try:
            cart_item_instance = self.cart_repo.get(cart_item_id)
            if cart_item_instance:
                self.cart_repo.delete(cart_item_instance)
            else:
                raise ValueError("Cart item not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
