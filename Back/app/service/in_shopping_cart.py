from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.buyer import BuyerService
from app.schemas.in_shopping_cart import InShoppingCartCreate, InShoppingCartUpdate
from app.models.in_shopping_cart import InShoppingCart
from app.crud_repository import CRUDRepository
from app.service.seller_product import SellerProductService


class InShoppingCartRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=InShoppingCart)
        self._model = InShoppingCart

    def delete_by_id(self, *, id_buyer, id_seller_product):
        self._db.query(self._model).filter(
            self._model.id_buyer == id_buyer,
            self._model.id_seller_product == id_seller_product,
        ).delete()
        self._db.commit()

    def get_by_id(self, *, id_buyer, id_seller_product) -> InShoppingCart:
        return (
            self._db.query(self._model)
            .filter(
                self._model.id_buyer == id_buyer,
                self._model.id_seller_product == id_seller_product,
            )
            .first()
        )
    
    def get_by_id_buyer(self, *, id_buyer) -> list[InShoppingCart]:
        return (
            self._db.query(self._model)
            .filter(
                self._model.id_buyer == id_buyer
            )
            .all()
        )
    
    def delete_by_id_buyer(self, *, id_buyer):
            self._db.query(self._model).filter(
                self._model.id_buyer == id_buyer).delete()
            self._db.commit()
    
    def update(self, entity, new_entity, exclude_defaults: bool = True):
        data = new_entity.model_dump(
            exclude_unset=True, exclude_defaults=exclude_defaults
        )
        self._db.query(self._model).filter(self._model.id_buyer == entity.id_buyer, self._model.id_seller_product == entity.id_seller_product).update({**data})  # type: ignore
        self._db.commit()
        self._db.refresh(entity)
        return entity


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
        self, id_buyer, shopping_cart_product: InShoppingCartCreate
    ) -> InShoppingCart:
        buyer = self.buyer_service.get_by_id(id_buyer)
        seller_product = self.seller_product_service.get_by_id(
            shopping_cart_product.id_seller_product
        )

        if self.cart_repo.get_where(InShoppingCart.id_buyer==id_buyer, InShoppingCart.id_seller_product==shopping_cart_product.id_seller_product):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in shopping cart",
            )

        if seller_product.quantity < shopping_cart_product.quantity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough seller products",
            )

        cart_product = InShoppingCart(
            **shopping_cart_product.model_dump(), id_buyer=id_buyer
        )
        self.cart_repo.add(cart_product)
        return cart_product

    def get_by_id(self, id_buyer, id_seller_product) -> InShoppingCart:
        if cart_item := self.cart_repo.get_by_id(
            id_buyer=id_buyer, id_seller_product=id_seller_product
        ):
            return cart_item

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id_seller_product={id_seller_product} and id_buyer={id_buyer} not found.",
        )

    def get_all(self) -> list[InShoppingCart]:
        return self.cart_repo.get_all()

    def update(
        self, id_buyer, id_seller_product, new_data: InShoppingCartUpdate
    ) -> InShoppingCart:
        cart_item = self.get_by_id(id_buyer, id_seller_product)
        seller_product = self.seller_product_service.get_by_id(id_seller_product)
        if new_data.quantity > seller_product.quantity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough seller products",
            )
        return self.cart_repo.update(cart_item, new_data)

    def delete_by_id(self, id_buyer, id_seller_product):
        self.get_by_id(id_buyer, id_seller_product)
        self.cart_repo.delete_by_id(
            id_buyer=id_buyer, id_seller_product=id_seller_product
        )

    def delete_all(self):
        self.cart_repo.delete_all()

    def get_by_id_buyer(self, id_buyer)-> list[InShoppingCart]:
        return self.cart_repo.get_by_id_buyer(id_buyer=id_buyer)
    
    def delete_by_id_buyer(self, id_buyer):
        return self.cart_repo.delete_by_id_buyer(id_buyer=id_buyer)
