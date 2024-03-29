from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.seller_product import SellerProductService
from app.service.buyer import BuyerService
from app.schemas.in_wish_list import InWishListCreate
from app.models.in_wish_list import InWishList
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

    def get_by_id(self, *, id_buyer, id_seller_product) -> InWishList:
        return (
            self._db.query(self._model)
            .filter(
                self._model.id_buyer == id_buyer,
                self._model.id_seller_product == id_seller_product,
            )
            .first()
        )


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
        buyer = self.buyer_service.get_by_id(id_buyer)
        self.seller_product_service.get_by_id(wish_list_item.id_seller_product)

        wl_item = InWishList(**wish_list_item.model_dump(), id_buyer=id_buyer)
        self.wishlist_repo.add(wl_item)
        buyer.in_wish_list.append(wl_item)
        self.session.commit()
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

    # def filter_wishlist_items(self, *expressions):
    #     try:
    #         return self.wishlist_repo.filter(*expressions)
    #     except Exception as e:
    #         raise e
    #     finally:
    #         self.session.close()

    # # probably won't need to use this
    # def update_wishlist_item(self, id_seller_product, id_buyer, new_data):
    #     try:
    #         composite_key = (id_seller_product, id_buyer)
    #         wishlist_item_instance = self.wishlist_repo.get(composite_key)
    #         if wishlist_item_instance:
    #             self.wishlist_repo.update(wishlist_item_instance, new_data)
    #             return wishlist_item_instance
    #         else:
    #             raise ValueError("Wishlist item not found.")
    #     except Exception as e:
    #         raise e
    #     finally:
    #         self.session.close()

    def delete_by_id(self, id_seller_product, id_buyer):
        self.wishlist_repo.delete_by_id(
            id_buyer=id_buyer, id_seller_product=id_seller_product
        )

    # We probably will never use this
    def delete_all(self):
        self.wishlist_repo.delete_all()
