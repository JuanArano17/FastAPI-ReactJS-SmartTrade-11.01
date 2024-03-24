from sqlalchemy.orm import Session
from app.models.in_wish_list import InWishList
from app.repository import Repository


class InWishListService:
    def __init__(self, session: Session):
        self.session = session
        self.wishlist_repo = Repository(session, InWishList)

    def add_to_wishlist(self, id_product, id_buyer):
        try:
            return self.wishlist_repo.add(id_product=id_product, id_buyer=id_buyer)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_wishlist_items(self):
        try:
            return self.wishlist_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_wishlist_item(self, wishlist_item_id):
        try:
            return self.wishlist_repo.get(wishlist_item_id)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_wishlist_items(self, *expressions):
        try:
            return self.wishlist_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def update_wishlist_item(self, wishlist_item_id, new_data):
        try:
            wishlist_item_instance = self.wishlist_repo.get(wishlist_item_id)
            if wishlist_item_instance:
                self.wishlist_repo.update(wishlist_item_instance, new_data)
                return wishlist_item_instance
            else:
                raise ValueError("Wishlist item not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_wishlist_item(self, wishlist_item_id):
        try:
            wishlist_item_instance = self.wishlist_repo.get(wishlist_item_id)
            if wishlist_item_instance:
                self.wishlist_repo.delete(wishlist_item_instance)
            else:
                raise ValueError("Wishlist item not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
