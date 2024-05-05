from app.models.users.types.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.users.types.buyer import BuyerService
from app.schemas.users.in_shopping_cart import (
    CompleteShoppingCart,
    InShoppingCartCreate,
    InShoppingCartUpdate,
)
from app.models.users.in_shopping_cart import InShoppingCart
from app.crud_repository import CRUDRepository
from app.service.products.seller_product import SellerProductService


class InShoppingCartRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=InShoppingCart)
        self._model = InShoppingCart

    def get_by_id_buyer(self, *, id_buyer) -> list[InShoppingCart]:
        return (
            self._db.query(self._model).filter(self._model.id_buyer == id_buyer).all()
        )

    def delete_by_id_buyer(self, *, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()
        self._db.commit()


class InShoppingCartService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        seller_product_service: SellerProductService,
    ):
        self.session = session
        self.cart_repo = InShoppingCartRepository(session=session)
        self.buyer_service = buyer_service
        self.seller_product_service = seller_product_service

    def add(
        self, id_buyer, shopping_cart_product: InShoppingCartCreate, id_size=None
    ) -> InShoppingCart:
        self.buyer_service.get_by_id(id_buyer)
        seller_product = self.seller_product_service.get_by_id(
            shopping_cart_product.id_seller_product
        )


        if seller_product.quantity < shopping_cart_product.quantity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough seller products",
            )
        
        
        if(seller_product.sizes==[]):
            if(id_size):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This shopping cart item shouldn't have a size assigned",
                )
            
            if self.cart_repo.get_where(
            InShoppingCart.id_buyer == id_buyer,
            InShoppingCart.id_seller_product == shopping_cart_product.id_seller_product,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product already in shopping cart",
                )
            
            cart_product = InShoppingCart(
                **shopping_cart_product.model_dump(), id_buyer=id_buyer
            )
            
        if(seller_product.sizes!=[]):
            if not id_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This shopping cart item should have a size assigned",
                )
            
            size=self.seller_product_service.size_repo.get_by_id(id_size)

            if(not size):
                raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Could not find size",
                            )

            if(shopping_cart_product.id_seller_product!=size.seller_product_id):
                raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This size doesn't belong to this product",
                            )

            if shopping_cart_product.quantity > size.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Not enough seller products",
                    )

            same_items=self.cart_repo.get_where(InShoppingCart.id_buyer==id_buyer, InShoppingCart.id_seller_product
                                                               == shopping_cart_product.id_seller_product)
                
            if same_items:
                for item in same_items:
                    #Compare same sizes
                    size2=self.seller_product_service.size_repo.get_by_id(item.id_size)
                    if(size2.size==size.size):
                        raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Product already in shopping cart",
                    )    
                                                                
            cart_product = InShoppingCart(
                **shopping_cart_product.model_dump(), id_buyer=id_buyer, id_size=id_size
            )
        
        cart_item = self.cart_repo.add(cart_product)
        return cart_item
        

    def add_by_user(
        self, user: User, shopping_cart_product: InShoppingCartCreate, id_size=None
    ) -> CompleteShoppingCart:
        buyer = self.buyer_service.get_by_id(user.id)

        seller_product = self.seller_product_service.get_by_id(
            shopping_cart_product.id_seller_product
        )

        if(seller_product.sizes!=[]):
            cart_product = self.add(
                id_buyer=buyer.id, shopping_cart_product=shopping_cart_product, id_size=id_size
            )
        else: 
            cart_product = self.add(
                id_buyer=buyer.id, shopping_cart_product=shopping_cart_product
            )

        seller_product = self.seller_product_service.get_by_id(
            cart_product.id_seller_product
        )
        complete_seller_product = (
            self.seller_product_service.map_seller_product_to_read_schema(
                seller_product
            )
        )

        size=None
        if(seller_product.sizes!=[]) :
                size=self.seller_product_service.size_repo.get_by_id(id_size)

        return CompleteShoppingCart(
            **cart_product.__dict__, seller_product=complete_seller_product, size=size
        )

    def get_by_id(self, id) -> InShoppingCart:
        if cart_item := self.cart_repo.get_by_id(
            id=id
        ):
            return cart_item

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id {id} not found.",
        )

    # def _get_by_id(self, id_buyer, id_seller_product) -> CompleteShoppingCart:
    #     cart_item = self.cart_repo.get_by_id(id_buyer=id_buyer, id_seller_product=id_seller_product)

    #     if not cart_item:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Cart item with id_seller_product={id_seller_product} and id_buyer={id_buyer} not found.",
    #         )

    #     seller_product = self.seller_product_service.get_by_id(id_seller_product)
    #     complete_seller_product = self.seller_product_service.map_seller_product_to_read_schema(seller_product)
    #     return CompleteShoppingCart(**cart_item.__dict__, seller_product=complete_seller_product)

    def get_by_id_buyer(self, id_buyer) -> list[InShoppingCart]:
        return self.cart_repo.get_by_id_buyer(id_buyer=id_buyer)

    def get_by_user(self, user: User) -> list[CompleteShoppingCart]:
        buyer = self.buyer_service.get_by_id(user.id)
        shopping_cart = []

        for cart_item in self.get_by_id_buyer(buyer.id):
            seller_product = self.seller_product_service.get_by_id(
                cart_item.id_seller_product
            )
            complete_seller_product = (
                self.seller_product_service.map_seller_product_to_read_schema(
                    seller_product
                )
            )

            size=self.seller_product_service.size_repo.get_by_id(cart_item.id_size)
            shopping_cart.append(
                CompleteShoppingCart(
                    **cart_item.__dict__, seller_product=complete_seller_product, size=size
                )
            )

        return shopping_cart

    def get_all(self) -> list[InShoppingCart]:
        return self.cart_repo.get_all()

    def update(
        self, id , new_data: InShoppingCartUpdate
    ) -> InShoppingCart:
        cart_item = self.get_by_id(id)
        seller_product = self.seller_product_service.get_by_id(cart_item.id_seller_product)
        
        if(seller_product.sizes==[]):
            if(new_data.id_size):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This shopping cart item shouldn't have a size assigned",
                )
            
            if new_data.quantity > seller_product.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Not enough seller products",
                )
            
            if self.cart_repo.get_where(
            InShoppingCart.id_buyer == new_data.id_buyer,
            InShoppingCart.id_seller_product == new_data.id_seller_product,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product already in shopping cart",
                )
        else:
            if(new_data.id_size):
                size=self.seller_product_service.size_repo.get_by_id(new_data.id_size)
                if(not size):
                    raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Could not find size",
                                )
                same_items=self.cart_repo.get_where(InShoppingCart.id_buyer==cart_item.id_buyer, InShoppingCart.id_seller_product
                                                               == cart_item.id_seller_product)
                
                size=self.seller_product_service.size_repo.get_by_id(new_data.id_size)
                if same_items and new_data.id_size!=cart_item.id_size:
                    for item in same_items:
                        size2=self.seller_product_service.size_repo.get_by_id(item.id_size)
                        if(size2.size==size.size):
                            raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product already in shopping cart",
                            )
                        
                if(new_data.id_size!=cart_item.id_size):
                    if cart_item.id_seller_product!=size.seller_product_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This size doesn't belong to this product",
                            )
                    
                if(not new_data.quantity):
                    if size.quantity<cart_item.quantity:
                        new_data.quantity=size.quantity
            
            else: 
                size=self.seller_product_service.size_repo.get_by_id(cart_item.id_size)

            if new_data.quantity and new_data.quantity > size.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Not enough seller products",
                    )
                

        return self.cart_repo.update(cart_item, new_data)

    def update_by_user(
        self, user: User, id, new_data: InShoppingCartUpdate
    ) -> CompleteShoppingCart:
        buyer = self.buyer_service.get_by_id(user.id)
        cart_item=self.get_by_id(id)
        if(cart_item.id_buyer!=user.id):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This cart item does not belong to the user.",
        )

        cart_item = self.update(id, new_data)
        seller_product = self.seller_product_service.get_by_id(
            cart_item.id_seller_product
        )
        complete_seller_product = (
            self.seller_product_service.map_seller_product_to_read_schema(
                seller_product
            )
        )
        if(seller_product.sizes==[]):
            return CompleteShoppingCart(
                **cart_item.__dict__, seller_product=complete_seller_product
            )
        elif seller_product.sizes!=[]:
            size=self.seller_product_service.size_repo.get_by_id(cart_item.id_size)
            return CompleteShoppingCart(
                    **cart_item.__dict__, seller_product=complete_seller_product, size=size
                )

    def delete_by_id(self, id_shopping_cart):
        self.cart_repo.delete_by_id(
            id=id_shopping_cart
        )

    def delete_all(self):
        self.cart_repo.delete_all()

    def delete_all_by_user(self, user: User):
        buyer = self.buyer_service.get_by_id(user.id)
        self.cart_repo.delete_by_id_buyer(id_buyer=buyer.id)

    def delete_by_id_buyer(self, id_buyer):
        return self.cart_repo.delete_by_id_buyer(id_buyer=id_buyer)

    def delete_one_by_user(self, user: User, id_shopping_cart):
        buyer = self.buyer_service.get_by_id(user.id)
        cart_item=self.get_by_id(id_shopping_cart)
        if(cart_item.id_buyer!=user.id):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This cart item does not belong to the user.",
        )
        self.get_by_id(id_shopping_cart) 
        self.delete_by_id(id_shopping_cart)
