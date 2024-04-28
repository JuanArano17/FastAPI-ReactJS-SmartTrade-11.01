from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUserDep, SellerProductServiceDep
from app.schemas.products.seller_product import (
    SellerProduct,
    SellerProductCreate,
    SellerProductRead,
    SellerProductUpdate,
)

router = APIRouter(
    prefix="/product/{product_id}/seller_products", tags=["Seller Products"]
)


@router.get(
    "/", response_model=list[SellerProductRead], response_model_exclude_none=True
)
async def read_seller_products(
    *, product_id: int, seller_product_service: SellerProductServiceDep
):
    """
    Retrieve seller products from product.
    """
    return seller_product_service.get_by_id_product(id_product=product_id)


@router.delete("/")
async def delete_seller_products(
    product_id: int, seller_product_service: SellerProductServiceDep
):
    """
    Delete all seller products.
    """
    return seller_product_service.delete_by_id_product(id_product=product_id)


seller_prod_router = APIRouter(prefix="/seller_products", tags=["Seller Products"])


@seller_prod_router.get(
    "/", response_model=list[SellerProductRead], response_model_exclude_none=True
)
async def read_seller_products_pure(*, seller_product_service: SellerProductServiceDep):
    """
    Retrieve seller products.
    """
    return seller_product_service.get_all_by_state("Approved")


@seller_prod_router.get(
    "/{seller_product_id}",
    response_model=SellerProductRead,
    response_model_exclude_none=True,
)
async def read_seller_product_by_id(
    seller_product_id: int, seller_product_service: SellerProductServiceDep
):
    """
    Retrieve a specific seller product.
    """
    seller_product = seller_product_service.get_by_id_full(seller_product_id)
    if seller_product is None:
        raise HTTPException(status_code=404, detail="Seller product not found")
    return seller_product


@seller_prod_router.post("/", response_model=SellerProduct)
async def create_seller_product(
    *,
    seller_id: int,
    seller_product: SellerProductCreate,
    seller_product_service: SellerProductServiceDep,
):
    """
    Create a new seller product.
    """
    return seller_product_service.add(
        id_seller=seller_id, seller_product=seller_product
    )


@seller_prod_router.delete("/{seller_product_id}")
async def delete_seller_product(
    *,
    seller_product_id: int,
    seller_product_service: SellerProductServiceDep,
):
    """
    Delete a seller product.
    """
    existing_seller_product = seller_product_service.get_by_id(
        seller_product_id=seller_product_id
    )

    if existing_seller_product is None:
        raise HTTPException(status_code=404, detail="Seller product not found")

    return seller_product_service.delete_by_id(seller_product_id)


@seller_prod_router.put("/{seller_product_id}", response_model=SellerProduct)
async def update_seller_product(
    *,
    seller_product_id: int,
    seller_product: SellerProductUpdate,
    seller_product_service: SellerProductServiceDep,
):
    """
    Update a seller product.
    """
    existing_seller_product = seller_product_service.get_by_id(
        seller_product_id=seller_product_id
    )

    if existing_seller_product is None:
        raise HTTPException(status_code=404, detail="Seller product not found")

    return seller_product_service.update(
        seller_product_id=seller_product_id, new_data=seller_product
    )


seller_router = APIRouter(
    prefix="/seller_products/me", tags=["Seller Products"]
)


@seller_router.get(
    "/", response_model=list[SellerProductRead], response_model_exclude_none=True
)
async def read_seller_products_from_seller(
    *, seller_product_service: SellerProductServiceDep, current_user:CurrentUserDep
):
    """
    Retrieve seller products from seller.
    """
    return seller_product_service.get_by_id_seller(current_user.id)