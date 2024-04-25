from fastapi import APIRouter

from app.api.routers import orders
from app.api.routers import cards
from app.api.routers import wish_list
from app.api.routers import shopping_cart
from app.api.routers import images
from app.api.routers import buyers
from app.api.routers import sellers
from app.api.routers import products
from app.api.routers import addresses
from app.api.routers import seller_product
from app.api.routers import login
from app.api.routers import users

api_router = APIRouter()
api_router.include_router(sellers.router)
api_router.include_router(buyers.router)
api_router.include_router(products.router)
api_router.include_router(addresses.router)
api_router.include_router(images.router)
api_router.include_router(images.image_router)
api_router.include_router(seller_product.router)
# api_router.include_router(seller_product.pure_router)
api_router.include_router(login.router)
# api_router.include_router(cards.router)
api_router.include_router(cards.cards_router)
# api_router.include_router(orders.router)
api_router.include_router(orders.orders_router)
api_router.include_router(orders.orders)
api_router.include_router(users.router)
# api_router.include_router(all_seller_product.router)
api_router.include_router(wish_list.list_token_router)
api_router.include_router(shopping_cart.cart_token_router)
api_router.include_router(seller_product.seller_prod_router)
