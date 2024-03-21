import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

Base = declarative_base()

from app.models.buyer import Buyer
from app.models.address import Address
from app.models.category import Category
from app.models.product import Product
from app.models.image import Image
from app.models.card import Card
from app.models.seller import Seller
from app.models.order import Order
from app.models.product_line import ProductLine
from app.models.seller_product import SellerProduct
from app.models.in_shopping_cart import InShoppingCart
from app.models.in_wish_list import InWishList
from app.models.refund_product import RefundProduct

load_dotenv()


def get_db_url() -> str:
    return os.getenv(
        "DB_URL",
        "postgresql+psycopg://postgres:password@localhost:5432/database",
    )


def get_engine() -> Engine:
    url = get_db_url()
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=True)
    return engine


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)
    return session
