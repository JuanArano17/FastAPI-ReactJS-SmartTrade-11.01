from typing import Any, Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import ProductServiceDep
from app.schemas.product import Product
from app.schemas.book import Book
from app.schemas.clothes import Clothes
from app.schemas.electrodomestics import Electrodomestics
from app.schemas.electronics import Electronics
from app.schemas.food import Food
from app.schemas.game import Game
from app.schemas.house_utilities import HouseUtilities

router = APIRouter(prefix="/products", tags=["products"])
class ProductResponse(BaseModel):
    product: Union[Book, Clothes, Electrodomestics, Electronics, Food, Game, HouseUtilities]
    category: str

@router.get(
    "/",
)
async def read_products(product_service: ProductServiceDep, category: Optional[str] = None):
    """
    Retrieve products.
    """
    return product_service.get_all_full(category)


@router.get(
    "/{product_id}"
)
async def read_product(*, product_id: int, product_service: ProductServiceDep):
    """
    Retrieve a product.
    """

    return product_service.get_by_id_full(product_id)
    

@router.post(
    "/",
    response_model=(
        Union[Game, Book, Food, Electronics, Electrodomestics, Clothes, HouseUtilities]
    ),
)
async def create_product(
    *, category_name: str, product: dict, product_service: ProductServiceDep
):
    """
    Create a new product.
    """
    return product_service.add(category=category_name, product_data=product)


@router.put(
    "/{product_id}",
    response_model=(
        Union[
            None,
            Game,
            Book,
            Food,
            Electronics,
            Electrodomestics,
            Clothes,
            HouseUtilities,
        ]
    ),
)
async def update_product(
    *, product_id: int, new_data: dict, product_service: ProductServiceDep
):
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
