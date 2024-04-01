from fastapi import APIRouter

from app.api.routers import shopping_cart
from app.api.routers import images
from app.api.routers import buyers
from app.api.routers import sellers
from app.api.routers import products
from app.api.routers import addresses

api_router = APIRouter()
api_router.include_router(sellers.router)
api_router.include_router(buyers.router)
api_router.include_router(products.router)
api_router.include_router(addresses.router)
api_router.include_router(images.router)
api_router.include_router(shopping_cart.router)