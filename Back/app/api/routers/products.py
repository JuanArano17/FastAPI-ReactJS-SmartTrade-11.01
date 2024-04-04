from fastapi import APIRouter

from app.schemas.product import Product, ProductCreate, ProductUpdate
from database import get_session
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


@router.get("/{product_id}")
async def read_product(*, product_id: int):
    """
    Retrieve a product.
    """
    return product_service.get_by_id(product_id)


@router.post("/")
async def create_product(*, category_name:str , product: dict):
    """
    Create a new product.
    """
    return product_service.add(category=category_name, product_data=product)


@router.put("/{product_id}")
async def update_product(*, product_id: int, product: dict):
    """
    Update a product.
    """
    return product_service.update(product_id,product)


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
