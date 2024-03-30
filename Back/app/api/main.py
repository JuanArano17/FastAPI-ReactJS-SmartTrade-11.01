from fastapi import APIRouter

from app.api.routers import sellers

api_router = APIRouter()
api_router.include_router(sellers.router)
