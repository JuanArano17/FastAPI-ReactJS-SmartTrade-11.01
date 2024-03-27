from sqlalchemy.orm import Session
from app.models.in_shopping_cart import InShoppingCart
from app.repository import Repository
from service.seller_product import SellerProductService


class InShoppingCartService:
    def __init__(self, session: Session):
        self.session = session
        self.cart_repo = Repository(session, InShoppingCart)

    def add_to_cart(self, id_seller_product, id_buyer, quantity):
        try:
            seller_product_serv=SellerProductService(self.session)
            seller_product=seller_product_serv.get_seller_product(id_seller_product)
            seller_product_quantity=seller_product.quantity
            #when making an order using the shopping cart (logic layer), make sure to check that the quantity in the shopping cart is still available, or update shopping carts after each order maybe
            if(quantity>seller_product_quantity):
                raise Exception("Not enough seller products")
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

    def update_cart_item(self, id_seller_product, id_buyer, new_data):
        try:
            quantity = new_data.get("quantity")
            seller_product_serv=SellerProductService(self.session)
            seller_product=seller_product_serv.get_seller_product(id_seller_product)
            seller_product_quantity=seller_product.quantity
            if(quantity):
                if(quantity>seller_product_quantity):
                    raise Exception("Not enough seller products")
            composite_key = (id_seller_product, id_buyer)
            cart_item_instance = self.cart_repo.get(composite_key)
            if not cart_item_instance:
                raise ValueError("Cart item not found.")
            self.cart_repo.update(cart_item_instance, new_data)
            return cart_item_instance
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_cart_item(self, id_buyer, id_seller_product):
        try:
            composite_key = (id_seller_product, id_buyer)
            cart_item_instance = self.cart_repo.get(composite_key)
            if cart_item_instance:
                self.cart_repo.delete(cart_item_instance)
            else:
                raise ValueError("Cart item not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
