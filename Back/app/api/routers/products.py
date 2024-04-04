from typing import List, Union
from fastapi import APIRouter

from database import get_session
from schemas.book import Book, BookCreate, BookUpdate
from schemas.clothes import Clothes, ClothesCreate, ClothesUpdate
from schemas.electrodomestics import Electrodomestics, ElectrodomesticsCreate, ElectrodomesticsUpdate
from schemas.electronics import Electronics, ElectronicsCreate, ElectronicsUpdate
from schemas.food import Food, FoodCreate, FoodUpdate
from schemas.game import Game, GameCreate, GameUpdate
from schemas.house_utilities import HouseUtilities, HouseUtilitiesCreate, HouseUtilitiesUpdate
from service.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])

session=get_session()
product_service=ProductService(session=session)

@router.get("/")
async def read_products():
    """
    Retrieve products.
    """
    return product_service.get_all()


@router.get("/{product_id}", response_model=(Union[Game,Book,Food,HouseUtilities,Electronics,Electrodomestics,Clothes]))
async def read_product(*, product_id: int):
    """
    Retrieve a product.
    """
    return product_service.product_repo.get_by_id(product_id)


@router.post("/", response_model=(Union[Game,Book,Food,HouseUtilities,Electronics,Electrodomestics,Clothes]))
async def create_product(*, category_name:str , product: dict):
    """
    Create a new product.
    """
    return product_service.add(category=category_name, product_data=product)


@router.put("/{product_id}", response_model=(Union[None,Game,Book,Food,HouseUtilities,Electronics,Electrodomestics,Clothes]))
async def update_product(*, product_id: int, new_data: dict):
    """
    Update a product.
    """
    return product_service.update(product_id, new_data)


@router.delete("/{product_id}")
async def delete_product(*, product_id: int):
    """
    Delete a product.
    """
    return product_service.delete_by_id(product_id)


@router.delete("/")
async def delete_products():
    """
    Delete all products.
    """
    return product_service.delete_all()
