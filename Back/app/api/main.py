from fastapi import APIRouter

from api.routers import cards
from app.api.routers import wish_list
from app.api.routers import shopping_cart
from app.api.routers import images
from app.api.routers import buyers
from app.api.routers import sellers
from app.api.routers import products
from app.api.routers import addresses
from app.api.routers import seller_product
from app.api.routers import login

api_router = APIRouter()
api_router.include_router(sellers.router)
api_router.include_router(buyers.router)
api_router.include_router(products.router)
api_router.include_router(addresses.router)
api_router.include_router(images.router)
api_router.include_router(shopping_cart.router)
api_router.include_router(wish_list.router)
api_router.include_router(seller_product.router)
api_router.include_router(login.router)
api_router.include_router(cards.router)
