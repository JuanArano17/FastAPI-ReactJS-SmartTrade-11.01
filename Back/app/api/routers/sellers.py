from fastapi import APIRouter

from app.api.deps import SellerProductServiceDep, SellerServiceDep
from app.schemas.users.types.seller import Seller, SellerCreate, SellerUpdate
from schemas.products.seller_product import SellerProductRead

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.get("/", response_model=list[Seller])
async def read_sellers(seller_service: SellerServiceDep):
    """
    Retrieve sellers.
    """
    return seller_service.get_all()


@router.get("/{seller_id}", response_model=Seller)
async def read_seller(*, seller_id: int, seller_service: SellerServiceDep):
    """
    Retrieve a seller.
    """
    return seller_service.get_by_id(seller_id)


@router.post("/", response_model=Seller)
async def create_seller(*, seller: SellerCreate, seller_service: SellerServiceDep):
    """
    Create a new seller.
    """
    return seller_service.add(seller)


@router.put("/{seller_id}", response_model=Seller)
async def update_seller(
    *, seller_id: int, seller: SellerUpdate, seller_service: SellerServiceDep
):
    """
    Update a seller.
    """
    return seller_service.update(seller_id, seller)


@router.delete("/{seller_id}")
async def delete_seller(*, seller_id: int, seller_service: SellerServiceDep):
    """
    Delete a seller.
    """
    return seller_service.delete_by_id(seller_id)


@router.delete("/")
async def delete_sellers(seller_service: SellerServiceDep):
    """
    Delete all sellers.
    """
    return seller_service.delete_all()

@router.get(
    "/{seller_id}/products", response_model=list[SellerProductRead], response_model_exclude_none=True
)
async def read_seller_products(
    *, seller_id: int, seller_product_service: SellerProductServiceDep
):
    """
    Retrieve seller products from product.
    """
    return seller_product_service.get_by_id_seller(id_seller=seller_id)
