from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Product
from app.crud_repository import CRUDRepository
from app.models.book import Book
from app.models.game import Game
from schemas.book import BookCreate, BookUpdate
from schemas.game import GameCreate, GameUpdate


class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.product_repo = CRUDRepository(session=session, model=Product)
        self.game_repo = CRUDRepository(session=session, model=Game)
        self.book_repo = CRUDRepository(session=session, model=Book)
        self.product_factory=ProductFactory(service=self)

    def add(self, category:str, product_data: dict):
        return self.product_factory.create_product(category=category, product_data=product_data)

    def get_by_id(self, product_id):
        #if product := self.product_repo.get_by_id(product_id):
        #    return product
        if product := self.product_factory.get_product_by_id(product_id=product_id):
            return product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    def get_all(self) -> list[Product]:
        return self.product_factory.get_all()

    def update(self, product_id, new_data: dict):
        product = self.get_by_id(product_id)
        return self.product_factory.update_product(product, new_data)

    def delete_by_id(self, product_id):
        #self.product_repo.delete_by_id(product_id)
        self.product_repo.delete_by_id(id=product_id)

    def delete_all(self):
        self.product_repo.delete_all()

class ProductFactory:
    def __init__ (self, service:ProductService):
        self.service=service

    def create_product(self, category: str, product_data: dict):
        if category.lower() == 'book':
            product = BookCreate(**product_data)
            return self.service.book_repo.add(Book(**product.model_dump()))
        elif category.lower() == 'game':
            product = GameCreate(**product_data)
            return self.service.game_repo.add(Game(**product.model_dump()))
        else:
            raise ValueError("Invalid product category")
        
    def update_product(self, product: Product, new_data: dict):
        if product.category.lower() == 'book':
            book = BookUpdate(**new_data)
            return self.service.book_repo.update(product, book)
        elif product.category.lower() == 'game':
            game = GameUpdate(**new_data)
            return self.service.game_repo.update(product, game)

    def get_product_by_id(self, product_id: int):
        product=self.service.product_repo.get_by_id(product_id)
        if product.category.lower() == 'book':
            return self.service.book_repo.get_by_id(product_id)
        elif product.category.lower() == 'game':
            return self.service.game_repo.get_by_id(product_id)

    def get_all(self):
        products=self.service.game_repo.get_all()
        products+=self.service.book_repo.get_all()
        return products
    

