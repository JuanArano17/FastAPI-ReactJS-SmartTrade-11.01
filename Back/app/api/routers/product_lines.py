from datetime import date
from fastapi import APIRouter
from sqlalchemy import Date

from app.api.deps import CurrentUserDep, ProductLineServiceDep
from app.schemas.orders.product_line import CompleteProductLine, ProductLine, ProductLineUpdate

router = APIRouter(prefix="/product_lines/me", tags=["ProductLines"])


@router.get("/", response_model=list[CompleteProductLine])
async def get_product_line(
    current_user: CurrentUserDep,
    product_line_service: ProductLineServiceDep,
):
    """
    Get all product lines from the current seller (the ones that dont have an estimated date, so that the seller may give them an estimated date)
    """
    return product_line_service.get_all_by_seller_id(current_user.id)


@router.post("/{product_line_id}", response_model=ProductLine, status_code=200)
async def add_estimated_date(
    current_user: CurrentUserDep,
    product_line_service: ProductLineServiceDep,
    product_line_id: int,
    estimated_date: ProductLineUpdate
):
    """
    Create an estimated date of arrival for the product line.
    """
    return product_line_service.add_estimated_date(product_line_id,current_user, estimated_date)