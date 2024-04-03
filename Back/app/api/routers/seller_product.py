from fastapi import APIRouter, HTTPException

from app.database import get_db
from app.schemas.seller_product import (
    SellerProduct,
    SellerProductCreate,
    SellerProductUpdate,
)
from app.service.product import ProductService
from app.service.seller import SellerService
from app.service.seller_product import SellerProductService
from app.service.user import UserService

router = APIRouter(
    prefix="/product/{product_id}/seller_products", tags=["seller-products"]
)

session = get_db()
user_service = UserService(session=session)
product_service = ProductService(session=session)
seller_service = SellerService(session=session, user_service=user_service)
seller_product_service = SellerProductService(
    session=session, seller_service=seller_service, product_service=product_service
)


@router.get("/", response_model=list[SellerProduct])
async def read_seller_products(*, product_id: int):
    """
    Retrieve seller products.
    """
    return seller_product_service.get_by_id_product(id_product=product_id)


@router.post("/", response_model=SellerProduct)
async def create_seller_product(
    *, product_id: int, seller_id: int, seller_product: SellerProductCreate
):
    """
    Create a new seller product.
    """
    if seller_product is None or seller_product.id_product != product_id:
        raise HTTPException(status_code=404, detail="Product not correct")
    return seller_product_service.add(
        id_seller=seller_id, seller_product=seller_product
    )


@router.delete("/")
async def delete_seller_products(product_id: int):
    """
    Delete all seller products.
    """
    return seller_product_service.delete_by_id_product(id_product=product_id)


@router.get("/{seller_product_id}", response_model=SellerProduct)
async def read_seller_product(*, product_id: int, seller_product_id: int):
    """
    Retrieve a specific seller product.
    """

    seller_product = seller_product_service.get_by_id(seller_product_id)

    if seller_product is None or seller_product.id_product != product_id:
        raise HTTPException(status_code=404, detail="Seller product not found")

    return seller_product


@router.put("/{seller_product_id}", response_model=SellerProduct)
async def update_seller_product(
    *, product_id=int, seller_product_id: int, seller_product: SellerProductUpdate
):
    """
    Update a seller product.
    """
    existing_seller_product = seller_product_service.get_by_id(
        seller_product_id=seller_product_id
    )

    if existing_seller_product is None or existing_seller_product.id_product != int(
        product_id
    ):
        raise HTTPException(status_code=404, detail="Seller product not found")

    return seller_product_service.update(
        seller_product_id=seller_product_id, new_data=seller_product
    )


@router.delete("/{seller_product_id}")
async def delete_seller_product(*, product_id=int, seller_product_id: int):
    """
    Delete a seller product.
    """
    existing_seller_product = seller_product_service.get_by_id(
        seller_product_id=seller_product_id
    )

    if existing_seller_product is None or existing_seller_product.id_product != int(
        product_id
    ):
        raise HTTPException(status_code=404, detail="Seller product not found")

    return seller_product_service.delete_by_id(seller_product_id)
