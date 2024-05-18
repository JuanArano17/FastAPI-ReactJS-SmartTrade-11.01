import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

# Base = declarative_base()
from app.models.users.country import Country
from app.models.users.types.user import User
from app.models.users.types.admin import Admin
from app.models.users.types.buyer import Buyer
from app.models.products.categories.book import Book
from app.models.products.categories.game import Game
from app.models.products.categories.electronics import Electronics
from app.models.products.categories.electrodomestics import Electrodomestics
from app.models.products.categories.house_utilities import HouseUtilities
from app.models.products.categories.clothes import Clothes
from app.models.products.categories.food import Food
from app.models.users.address import Address
from app.models.products.product import Product
from app.models.products.image import Image
from app.models.users.card import Card
from app.models.users.types.seller import Seller
from app.models.orders.order import Order
from app.models.orders.product_line import ProductLine
from app.models.products.categories.variations.size import Size
from app.models.products.seller_product import SellerProduct
from app.models.users.in_shopping_cart import InShoppingCart
from app.models.users.in_wish_list import InWishList
from app.models.orders.refund_product import RefundProduct
from app.models.products.review import Review

load_dotenv()


def get_db_url() -> str:
    return os.getenv(
        "DB_URL",
        #"postgresql+psycopg://postgres:password@database-1.caonuyb119ll.us-east-1.rds.amazonaws.com:5432/remote_db", 
        "postgresql+psycopg://postgres:password@localhost:5432/database",
    )


def get_engine() -> Engine:
    url = get_db_url()
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


engine = create_engine(get_db_url(), pool_size=50, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
