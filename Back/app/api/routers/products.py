from fastapi import APIRouter

from app.api.deps import ProductServiceDep
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[Product])
async def read_products(product_service: ProductServiceDep):
    """
    Retrieve products.
    """
    return product_service.get_all()


@router.get("/{product_id}", response_model=Product)
async def read_product(*, product_id: int, product_service: ProductServiceDep):
    """
    Retrieve a product.
    """
    return product_service.get_by_id(product_id)


@router.post("/{category_id}", response_model=Product)
async def create_product(
    *, category_id: int, product: ProductCreate, product_service: ProductServiceDep
):
    """
    Create a new product.
    """
    return product_service.add(id_category=category_id, product=product)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    *, product_id: int, product: ProductUpdate, product_service: ProductServiceDep
):
    """
    Update a product.
    """
    return product_service.update(product_id, product)


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
