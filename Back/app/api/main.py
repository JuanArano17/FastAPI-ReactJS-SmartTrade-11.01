from fastapi import APIRouter

from app.api.routers import buyers
from app.api.routers import sellers
from app.api.routers import products

api_router = APIRouter()
api_router.include_router(sellers.router)
api_router.include_router(buyers.router)
api_router.include_router(products.router)
