from fastapi import APIRouter

from app.api.routers import buyers
from app.api.routers import sellers

api_router = APIRouter()
api_router.include_router(sellers.router)
api_router.include_router(buyers.router)
