from pydantic import ValidationError
from sqlalchemy.orm import Session, selectin_polymorphic
from fastapi import HTTPException, status
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select

from app.models.products.product import Product
from app.crud_repository import CRUDRepository
from app.models.products.categories.book import Book
from app.models.products.categories.game import Game
from app.models.products.categories.electronics import Electronics
from app.models.products.categories.clothes import Clothes
from app.models.products.categories.food import Food
from app.models.products.categories.house_utilities import HouseUtilities
from app.models.products.categories.electrodomestics import Electrodomestics
from app.schemas.products.categories.book import BookCreate, BookUpdate
from app.schemas.products.categories.clothes import ClothesCreate, ClothesUpdate
from app.schemas.products.categories.electrodomestics import (
    ElectrodomesticsCreate,
    ElectrodomesticsUpdate,
)
from app.schemas.products.categories.electronics import (
    ElectronicsCreate,
    ElectronicsUpdate,
)
from app.schemas.products.categories.food import FoodCreate, FoodUpdate
from app.schemas.products.categories.game import GameCreate, GameUpdate
from app.schemas.products.categories.house_utilities import (
    HouseUtilitiesCreate,
    HouseUtilitiesUpdate,
)
from app.schemas.products.product import ProductUpdate


class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.product_repo = CRUDRepository(session=session, model=Product)
        self.game_repo = CRUDRepository(session=session, model=Game)
        self.book_repo = CRUDRepository(session=session, model=Book)
        self.clothes_repo = CRUDRepository(session=session, model=Clothes)
        self.electronics_repo = CRUDRepository(session=session, model=Electronics)
        self.house_utilities_repo = CRUDRepository(
            session=session, model=HouseUtilities
        )
        self.food_repo = CRUDRepository(session=session, model=Food)
        self.electrodomestics_repo = CRUDRepository(
            session=session, model=Electrodomestics
        )
        self.product_factory = ProductFactory(service=self)

    def add(self, category: str, product_data: dict):
        return self.product_factory.create_product(
            category=category, product=product_data
        )

    def _get_product_dict(self, product: Product):
        category = product.__class__.__name__
        product_dict = product.__dict__
        product_dict["category"] = category
        product_dict.update(
            {
                column: getattr(product, column)
                for column in product.__table__.columns.keys()
            }
        )
        product_dict["seller_products"] = [
            seller_product.__dict__ for seller_product in product.seller_products
        ]
        product_dict["images"] = [image.__dict__ for image in product.images]
        return product_dict

    def get_by_id(self, product_id):
        # if product := self.product_repo.get_by_id(product_id):
        #    return product
        if product := self.product_repo.get_by_id(product_id):
            return product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    def get_by_id_full(self, product_id: int):
        product = self.get_by_id(product_id)
        return self._get_product_dict(product)

    def get_all_full(self, category):
        products = self.get_all()
        product_dicts = []
        for product in products:
            product_category = product.__class__.__name__.lower()
            if category is None or category.lower() == product_category:
                product_dicts.append(self._get_product_dict(product))
        return product_dicts

    def get_all(self) -> list[Product]:
        load_opt = selectin_polymorphic(
            Product,
            [Book, Game, Electronics, Clothes, Food, HouseUtilities, Electrodomestics],
        )
        return self.session.scalars(select(Product).options(load_opt)).all()

    def update(self, product_id, new_data: dict):
        return self.product_factory.update_product(product_id, new_data)

    def delete_by_id(self, product_id):
        # self.product_repo.delete_by_id(product_id)
        product = self.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found.",
            )
        self.product_repo.delete_by_id(id=product_id)

    def delete_all(self):
        self.product_repo.delete_all()


class ProductFactory:
    def __init__(self, service: ProductService):
        self.service = service

    def create_product(self, category: str, product: dict):
        try:
            if category.lower() == "book":
                book = BookCreate(**product)
                return self.service.book_repo.add(Book(**book.model_dump()))
            elif category.lower() == "game":
                game = GameCreate(**product)
                return self.service.game_repo.add(Game(**game.model_dump()))
            elif category.lower() == "clothes":
                clothes = ClothesCreate(**product)
                return self.service.clothes_repo.add(Clothes(**clothes.model_dump()))
            elif category.lower() == "electronics":
                electronics = ElectronicsCreate(**product)
                return self.service.electronics_repo.add(
                    Electronics(**electronics.model_dump())
                )
            elif category.lower() == "houseutilities":
                house_utilities = HouseUtilitiesCreate(**product)
                return self.service.house_utilities_repo.add(
                    HouseUtilities(**house_utilities.model_dump())
                )
            elif category.lower() == "food":
                food = FoodCreate(**product)
                return self.service.food_repo.add(Food(**food.model_dump()))
            elif category.lower() == "electrodomestics":
                electrodomestics = ElectrodomesticsCreate(**product)
                return self.service.electrodomestics_repo.add(
                    Electrodomestics(**electrodomestics.model_dump())
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid product category",
                )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
        except ProgrammingError as s:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(s)
            )

    def update_product(self, product_id: int, new_data: dict):
        product = self.service.get_by_id(product_id)
        # Extract common attributes from update_data
        # Extract common attributes from new_data
        common_attributes = {}
        for key in ["name", "description", "stock", "spec_sheet"]:
            if key in new_data:
                common_attributes[key] = new_data.pop(key)
        try:
            if len(common_attributes) != 0:
                product_update = ProductUpdate(**common_attributes)
                product = self.service.product_repo.update(product, product_update)

            if len(new_data) == 0:
                return product

            if product.category.lower() == "book":
                new_book_data = BookUpdate(**new_data)
                return self.service.book_repo.update(product, new_book_data)
            elif product.category.lower() == "game":
                new_game_data = GameUpdate(**new_data)
                return self.service.game_repo.update(product, new_game_data)
            elif product.category.lower() == "clothes":
                new_clothes_data = ClothesUpdate(**new_data)
                return self.service.clothes_repo.update(product, new_clothes_data)
            elif product.category.lower() == "electronics":
                new_electronics_data = ElectronicsUpdate(**new_data)
                return self.service.electronics_repo.update(
                    product, new_electronics_data
                )
            elif product.category.lower() == "houseutilities":
                new_house_utilities_data = HouseUtilitiesUpdate(**new_data)
                return self.service.house_utilities_repo.update(
                    product, new_house_utilities_data
                )
            elif product.category.lower() == "food":
                new_food_data = FoodUpdate(**new_data)
                return self.service.food_repo.update(product, new_food_data)
            elif product.category.lower() == "electrodomestics":
                new_electrodomestics_data = ElectrodomesticsUpdate(**new_data)
                return self.service.electrodomestics_repo.update(
                    product, new_electrodomestics_data
                )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
        except ProgrammingError as s:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(s)
            )

    def get_all(self):
        products = []
        games: list[Game] = []
        books: list[Book] = []
        foods: list[Food] = []
        electronics: list[Electronics] = []
        electrodomestics: list[Electrodomestics] = []
        clothes: list[Clothes] = []
        house_utilities: list[HouseUtilities] = []

        games += self.service.game_repo.get_all()
        books += self.service.book_repo.get_all()
        clothes += self.service.clothes_repo.get_all()
        electronics += self.service.electronics_repo.get_all()
        house_utilities += self.service.house_utilities_repo.get_all()
        foods += self.service.food_repo.get_all()
        electrodomestics += self.service.electrodomestics_repo.get_all()
        products = {
            "games": games,
            "books": books,
            "clothes": clothes,
            "electronics": electronics,
            "house_utilities": house_utilities,
            "foods": foods,
            "electrodomestics": electrodomestics,
        }
        return products
