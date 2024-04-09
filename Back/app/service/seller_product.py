from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.seller_product import SellerProductCreate, SellerProductUpdate
from app.service.seller import SellerService
from app.models.seller_product import SellerProduct
from app.crud_repository import CRUDRepository
from app.service.product import ProductService

class SellerProductRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=SellerProduct)
        self._model = SellerProduct

    def get_by_id_product(self, id_product) -> list[SellerProduct]:
        return (
            self._db.query(self._model).filter(self._model.id_product == id_product).all()
        )
    
    def delete_by_id_product(self, id_product):
        self._db.query(self._model).filter(self._model.id_product == id_product).delete()  # type: ignore
        self._db.commit()


class SellerProductService:
    def __init__(
        self,
        session: Session,
        seller_service: SellerService,
        product_service: ProductService,
    ):
        self.session = session
        self.seller_product_repo = SellerProductRepository(session=session)
        self.seller_service = seller_service
        self.product_service = product_service

    def add(self, id_seller, seller_product: SellerProductCreate) -> SellerProduct:
        self.seller_service.get_by_id(id_seller)
        product = self.product_service.get_by_id(seller_product.id_product)

        if self.seller_product_repo.get_where(
            SellerProduct.id_seller == id_seller,
            SellerProduct.id_product == seller_product.id_product,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller already has a product with id {seller_product.id_product}",
            )

        product.stock += seller_product.quantity  # type: ignore

        seller_product_obj = SellerProduct(
            **seller_product.model_dump(), id_seller=id_seller
        )
        seller_product_obj = self.seller_product_repo.add(seller_product_obj)
        return seller_product_obj

    def get_by_id(self, seller_product_id) -> SellerProduct:
        if seller_product := self.seller_product_repo.get_by_id(seller_product_id):
            return seller_product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller product with id {seller_product_id} not found.",
        )

    def get_all(self) -> list[SellerProduct]:
        return self.seller_product_repo.get_all()

    def update(self, seller_product_id, new_data: SellerProductUpdate) -> SellerProduct:
        seller_product = self.get_by_id(seller_product_id)

        if new_data.quantity:
            product = self.product_service.get_by_id(seller_product.id_product)
            product.stock += new_data.quantity - seller_product.quantity  # type: ignore
            seller_product.notify_observers(new_data.quantity)

        return self.seller_product_repo.update(seller_product, new_data)

    def delete_by_id(self, seller_product_id):
        seller_product = self.get_by_id(seller_product_id)
        product = self.product_service.get_by_id(seller_product.id_product)
        product.stock -= seller_product.quantity  # type: ignore
        self.seller_product_repo.delete_by_id(seller_product_id)

    def delete_all(self):
        seller_products = self.get_all()
        for seller_product in seller_products:
            product = self.product_service.get_by_id(seller_product.id_product)
            product.stock -= seller_product.quantity  # type: ignore
        self.seller_product_repo.delete_all()
    
    def get_by_id_product(self, id_product)-> list[SellerProduct]:
        return self.seller_product_repo.get_by_id_product(id_product=id_product)
    
    def delete_by_id_product(self, id_product):
        return self.seller_product_repo.delete_by_id_product(id_product=id_product)
