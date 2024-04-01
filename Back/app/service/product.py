from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from app.crud_repository import CRUDRepository

class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.product_repo = CRUDRepository(session=session, model=Product)

    def add(self, id_category: int, product: ProductCreate) -> Product:
        return self.product_repo.add(
            Product(**product.model_dump(), id_category=id_category)
        )

    def get_by_id(self, product_id) -> Product:
        if product := self.product_repo.get_by_id(product_id):
            return product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    def get_all(self) -> list[Product]:
        return self.product_repo.get_all()

    def update(self, product_id, new_data: ProductUpdate) -> Product:
        product = self.get_by_id(product_id)
        return self.product_repo.update(product, new_data)

    def delete_by_id(self, product_id):
        self.product_repo.delete_by_id(product_id)

    def delete_all(self):
        self.product_repo.delete_all()
