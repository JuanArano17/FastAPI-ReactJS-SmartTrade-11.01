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

@router.get(
    "/",
)
async def read_products(product_service: ProductServiceDep, category: Optional[str] = None):
    """
    Retrieve products.
    """
    products = product_service.get_all()
    product_dicts = []
    for product in products:
        product_category = product.__class__.__name__
        print(category)
        print(product_category)
        if category is None or category.lower() == product_category.lower():
            product_dict = product.__dict__
            product_dict['category'] = product_category
            
            # Get the list of seller products for the current product
            seller_products = [seller_product.__dict__ for seller_product in product.seller_products]
            product_dict['seller_products'] = seller_products
            
            # Get the list of images
            images = [image.__dict__ for image in product.images]
            product_dict['images'] = images
            
            product_dicts.append(product_dict)
    return product_dicts


@router.get(
    "/{product_id}"
)
async def read_product(*, product_id: int, product_service: ProductServiceDep):
    """
    Retrieve a product.
    """
    product =  product_service.get_by_id(product_id)
    category = product.__class__.__name__

     # Get attributes of the base class
    product_dict = product.__dict__

    # Add category to the product dictionary
    product_dict['category'] = category
    # Get attributes of the product that are specific to the category
    # Get attributes of the product as a dictionary
    product_dict.update({column: getattr(product, column) for column in product.__table__.columns.keys()})
    # Get the list of seller products
    seller_products = [seller_product.__dict__ for seller_product in product.seller_products]
    images = [image.__dict__ for image in product.images]
    product_dict['seller_products'] = seller_products
    product_dict['images'] = images
    return product_dict
    

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
