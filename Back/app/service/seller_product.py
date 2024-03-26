from sqlalchemy.orm import Session
from app.models.seller_product import SellerProduct
from app.repository import Repository
from service.product import ProductService


class SellerProductService:
    def __init__(self, session: Session):
        self.session = session
        self.seller_product_repo = Repository(session, SellerProduct)

    def add_seller_product(
        self, id_product, id_seller, quantity, price, shipping_costs
    ):
        try:
            # Check if the seller already owns an instance of this product
            exists_already = self.filter_seller_products(
                SellerProduct.id_seller == id_seller,
                SellerProduct.id_product == id_product,
            )
            if len(exists_already)>0:
                raise Exception("The seller already owns an instance of this product")

            # Add the seller product
            seller_product = self.seller_product_repo.add(
                id_product=id_product,
                id_seller=id_seller,
                quantity=quantity,
                price=price,
                shipping_costs=shipping_costs,
            )
            product_serv=ProductService(self.session)
            old_stock=product_serv.get_product(id_product).stock
            product_stock = old_stock + quantity
            product_serv.update_product(id_product, {"stock":product_stock})
            return seller_product
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def list_seller_products(self):
        try:
            return self.seller_product_repo.list()
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def get_seller_product(self, pk):
        try:
            return self.seller_product_repo.get(pk)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def filter_seller_products(self, *expressions):
        try:
            return self.seller_product_repo.filter(*expressions)
        except Exception as e:
            raise e
        finally:
            self.session.close()

    #this method assumes that we never change id_product or id_seller, which we probably won't have to
    def update_seller_product(self, seller_product_id, new_data):
        try:
            seller_product_instance = self.seller_product_repo.get(seller_product_id)
            # Check if the seller already owns an instance of this product
            id_product = new_data.get("id_product")
            id_seller = new_data.get("id_seller")
            quantity = new_data.get("quantity")
            old_quantity=seller_product_instance.quantity
            if(id_seller==None):
                id_seller=seller_product_instance.id_seller
            
            if(id_product==None):
                id_product=seller_product_instance.id_product

            # Check if the seller already owns an instance of this product
            exists_already = self.seller_product_repo.filter(
                SellerProduct.id != seller_product_id, # Exclude the current seller product being updated
                SellerProduct.id_seller == id_seller,
                SellerProduct.id_product == id_product,
            )

            if len(exists_already)>0:
                raise Exception("The seller already owns an instance of this product")
            
            if seller_product_instance:
                self.seller_product_repo.update(seller_product_instance, new_data)
                #return seller_product_instance
            else:
                raise ValueError("Seller product not found.")
            if(quantity):
                product_serv=ProductService(self.session)
                old_stock=product_serv.get_product(id_product).stock
                product_stock = old_stock - old_quantity + quantity
                product_serv.update_product(id_product, {"stock":product_stock})
            
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_seller_product(self, seller_product_id):
        try:
            seller_product_instance = self.seller_product_repo.get(seller_product_id)
            if seller_product_instance:
                self.seller_product_repo.delete(seller_product_instance)
            else:
                raise ValueError("Seller product not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
