import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.models.users.types.user import User
from app.service.buyer import BuyerService
from app.service.seller import SellerService
from app.service.user import UserService
from app.database import engine
from app.main import app
from app.service.address import AddressService
from app.service.card import CardService
from app.service.image import ImageService
from app.service.product import ProductService
from service.in_shopping_cart import InShoppingCartService
from service.in_wish_list import InWishListService
from service.seller_product import SellerProductService


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(autoflush=False, autocommit=False, bind=engine) as session:
        yield session
        session.execute(delete(User))
        session.commit()


@pytest.fixture(scope="function", autouse=True)
def clear(db):
    db.execute(delete(User))
    db.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def user_service(db):
    return UserService(session=db)


@pytest.fixture(scope="module")
def buyer_service(db, user_service):
    return BuyerService(session=db, user_service=user_service)


@pytest.fixture(scope="module")
def seller_service(db, user_service):
    return SellerService(session=db, user_service=user_service)


@pytest.fixture(scope="module")
def address_service(db, buyer_service):
    return AddressService(session=db, buyer_service=buyer_service)


@pytest.fixture(scope="module")
def card_service(db, buyer_service):
    return CardService(session=db, buyer_service=buyer_service)


@pytest.fixture(scope="module")
def product_service(db):
    return ProductService(session=db)


@pytest.fixture(scope="module")
def image_service(db, product_service):
    return ImageService(session=db, product_service=product_service)


@pytest.fixture(scope="module")
def seller_product_service(db, seller_service, product_service):
    return SellerProductService(
        session=db, seller_service=seller_service, product_service=product_service
    )


@pytest.fixture(scope="module")
def wish_list_service(db, seller_product_service, buyer_service):
    return InWishListService(
        session=db,
        seller_product_service=seller_product_service,
        buyer_service=buyer_service,
    )


@pytest.fixture(scope="module")
def shopping_cart_service(db, seller_product_service, buyer_service):
    return InShoppingCartService(
        session=db,
        buyer_service=buyer_service,
        seller_product_service=seller_product_service,
    )
