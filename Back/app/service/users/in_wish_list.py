from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.products.seller_product import SellerProductService
from app.service.users.types.buyer import BuyerService
from app.schemas.users.in_wish_list import InWishListCreate
from app.models.users.in_wish_list import InWishList
from app.crud_repository import CRUDRepository


class InWishListRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=InWishList)
        self._model = InWishList

    def delete_by_id(self, *, id_buyer, id_seller_product):
        self._db.query(self._model).filter(
            self._model.id_buyer == id_buyer,
            self._model.id_seller_product == id_seller_product,
        ).delete()
        self._db.commit()

    def get_by_id(self, *, id_buyer, id_seller_product) -> InWishList:
        return (
            self._db.query(self._model)
            .filter(
                self._model.id_buyer == id_buyer,
                self._model.id_seller_product == id_seller_product,
            )
            .first()
        )

    def get_by_id_buyer(self, *, id_buyer) -> list[InWishList]:
        return (
            self._db.query(self._model).filter(self._model.id_buyer == id_buyer).all()
        )

    def delete_by_id_buyer(self, *, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()
        self._db.commit()


class InWishListService:
    def __init__(
        self,
        session: Session,
        seller_product_service: SellerProductService,
        buyer_service: BuyerService,
    ):
        self.session = session
        self.wishlist_repo = InWishListRepository(session=session)
        self.seller_product_service = seller_product_service
        self.buyer_service = buyer_service

    def add(self, id_buyer, wish_list_item: InWishListCreate) -> InWishList:
        if self.wishlist_repo.get_where(
            InWishList.id_buyer == id_buyer,
            InWishList.id_seller_product == wish_list_item.id_seller_product,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in wish list",
            )
        self.buyer_service.get_by_id(id_buyer)
        self.seller_product_service.get_by_id(wish_list_item.id_seller_product)

        wl_item = InWishList(**wish_list_item.model_dump(), id_buyer=id_buyer)
        self.wishlist_repo.add(wl_item)
        return wl_item

    def get_by_id(self, id_seller_product, id_buyer) -> InWishList:
        if wl_item := self.wishlist_repo.get_by_id(
            id_buyer=id_buyer, id_seller_product=id_seller_product
        ):
            return wl_item

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found",
        )

    def get_all(self) -> list[InWishList]:
        return self.wishlist_repo.get_all()

    def get_all_by_buyer(self, id_buyer) -> list[InWishList]:
        return self.wishlist_repo.get_where(InWishList.id_buyer == id_buyer)

    def delete_by_id(self, id_seller_product, id_buyer):
        self.wishlist_repo.delete_by_id(
            id_buyer=id_buyer, id_seller_product=id_seller_product
        )

    # We probably will never use this
    def delete_all(self):
        self.wishlist_repo.delete_all()

    def get_by_id_buyer(self, id_buyer) -> list[InWishList]:
        return self.wishlist_repo.get_by_id_buyer(id_buyer=id_buyer)

    def delete_by_id_buyer(self, id_buyer):
        return self.wishlist_repo.delete_by_id_buyer(id_buyer=id_buyer)
