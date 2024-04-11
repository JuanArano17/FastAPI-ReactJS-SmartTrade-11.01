from typing import List, Union
from fastapi import APIRouter

from app.api.deps import ProductServiceDep
from app.schemas.product import Product
from schemas.book import Book
from schemas.clothes import Clothes
from schemas.electrodomestics import Electrodomestics
from schemas.electronics import Electronics
from schemas.food import Food
from schemas.game import Game
from schemas.house_utilities import HouseUtilities

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def read_products(product_service: ProductServiceDep):
    """
    Retrieve products.
    """
    return product_service.get_all()


@router.get("/{product_id}", response_model=(Union[Game,Book,Food,Electronics,Electrodomestics,Clothes,HouseUtilities]))
async def read_product(*, product_id: int, product_service: ProductServiceDep):
    """
    Retrieve a product.
    """
    return product_service.get_by_id(product_id)


@router.post("/", response_model=(Union[Game,Book,Food,Electronics,Electrodomestics,Clothes,HouseUtilities]))
async def create_product(*, category_name:str , product: dict, product_service: ProductServiceDep):
    """
    Create a new product.
    """
    return product_service.add(category=category_name, product_data=product)


@router.put("/{product_id}", response_model=(Union[None,Game,Book,Food,Electronics,Electrodomestics,Clothes,HouseUtilities]))
async def update_product(*, product_id: int, new_data: dict, product_service: ProductServiceDep):
    """
    Update a product.
    """
    return product_service.update(product_id, new_data)


@router.delete("/{product_id}")
async def delete_product(*, product_id: int, product_service: ProductServiceDep):
    """
    Delete a product.
    """
    return product_service.delete_by_id(product_id)


@router.delete("/")
async def delete_products(product_service: ProductServiceDep):
    """
    Delete all products.
    """
    return product_service.delete_all()
