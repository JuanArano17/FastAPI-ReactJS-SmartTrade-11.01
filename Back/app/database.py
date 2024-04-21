import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

# Base = declarative_base()
from app.models.users.types.user import User
from app.models.users.types.admin import Admin
from app.models.users.types.buyer import Buyer
from app.models.users.address import Address
from app.models.products.product import Product
from app.models.products.image import Image
from app.models.users.card import Card
from app.models.users.types.seller import Seller
from app.models.orders.order import Order
from app.models.orders.product_line import ProductLine
from app.models.products.seller_product import SellerProduct
from app.models.users.in_shopping_cart import InShoppingCart
from app.models.users.in_wish_list import InWishList
from app.models.orders.refund_product import RefundProduct

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


engine = create_engine(get_db_url(), pool_size=50, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
