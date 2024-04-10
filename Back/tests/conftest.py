import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.models.user import User
from app.service.buyer import BuyerService
from app.service.seller import SellerService
from app.service.user import UserService
from app.database import engine
from app.main import app
from service.address import AddressService
from service.card import CardService


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