from datetime import datetime
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users.card import Card
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.card import CardCreate
from app.service.users.types.buyer import BuyerService
from app.service.users.card import CardService


def fake_card():
    return {
        "card_number": "5555555555554444",
        "card_name": "Pedro Fernandez Gómez",
        "card_exp_date": datetime(2025, 1, 1).date().strftime("%Y-%m-%d"),
        "card_security_num": "123",
    }


def fake_buyer():
    return {
        "email": "mytestemail@gmail.com",
        "name": "Jonathan",
        "surname": "Wick Doe",
        "dni": "58263711F",
        "birth_date": "1993-02-02",
        "eco_points": 0,
        "billing_address": "Street Whatever 123",
        "payment_method": "Bizum",
        "password": "arandompassword",
    }


def test_create_card(
    client: TestClient,
    buyer_service: BuyerService,
    card_service: CardService,
    db: Session,
):
    data = fake_buyer()
    buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    card_data = fake_card()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/cards/me/", json=card_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["card_number"] == card_data["card_number"]
    assert content["card_name"] == card_data["card_name"]
    assert content["card_exp_date"] == card_data["card_exp_date"]
    assert "id" in content
    assert "id_buyer" in content
    assert "card_security_num" not in content

    card = card_service.get_by_id(content["id"])
    assert card is not None
    assert card.id_buyer == content["id_buyer"]


def test_create_card_invalid_data(client: TestClient, buyer_service: BuyerService):
    data = fake_buyer()
    buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    data["card_number"] = "1"  # Invalid card number

    response = client.post("/cards/me/", json=data, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_same_card_for_buyer(
    client: TestClient,
    buyer_service: BuyerService,
    card_service: CardService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    data = fake_card()
    card_service.add(buyer.id, CardCreate(**data))

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/cards/me/", json=data, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    card_num = data["card_number"]
    assert (
        content["detail"]
        == f"Card with number {card_num} already exists for buyer with id {buyer.id}."
    )


def test_get_card_by_id(
    client: TestClient,
    card_service: CardService,
    buyer_service: BuyerService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    card = card_service.add(buyer.id, CardCreate(**data))

    response = client.get(f"/cards/me/{card.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["card_number"] == data["card_number"]
    assert content["card_name"] == data["card_name"]
    assert content["card_exp_date"] == data["card_exp_date"]
    assert "id" in content
    assert "id_buyer" in content
    assert "card_security_num" not in content
    assert content["id"] == card.id
    assert content["id_buyer"] == card.id_buyer
    assert card.card_security_num == data["card_security_num"]


def test_get_card_not_found(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("cards/me/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert (
        content["detail"] == f"Card with id 999 not found for buyer with id {buyer.id}."
    )


def test_get_cards(
    client: TestClient,
    buyer_service: BuyerService,
    card_service: CardService,
    db: Session,
):
    john = buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
            birth_date="1990-11-11",
            dni="12345678A",
            eco_points=0,
            billing_address="Street Whatever 123",
            payment_method="Bizum",
            password="arandompassword",
        )
    )
    maria = buyer_service.add(
        BuyerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            birth_date="1990-11-11",
            dni="87654321B",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )

    card1 = card_service.add(
        john.id,
        CardCreate(
            card_number="5555555555554444",
            card_name="Pedro Fernandez Gómez",
            card_exp_date=datetime(2026, 2, 1).date(),
            card_security_num="333",
        ),
    )

    card2 = card_service.add(
        john.id,
        CardCreate(
            card_number="7618085117080457",
            card_name="Marta Garcia Gómez",
            card_exp_date=datetime(2025, 1, 1).date(),
            card_security_num="123",
        ),
    )
    card3 = card_service.add(
        maria.id,
        CardCreate(
            card_number="1517468977888257",
            card_name="Mario Perez Martinez",
            card_exp_date=datetime(2027, 9, 1).date(),
            card_security_num="193",
        ),
    )

    login_data = {"username": maria.email, "password": "mypass@123"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/cards/me", headers=headers)

    login_data = {"username": john.email, "password": "arandompassword"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response1 = client.get("/cards/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert card3.id in [address["id"] for address in content]
    assert response1.status_code == status.HTTP_200_OK
    content = response1.json()
    assert len(content) == 2
    assert card1.id in [address["id"] for address in content]
    assert card2.id in [address["id"] for address in content]


def test_update_card(
    client: TestClient,
    card_service: CardService,
    buyer_service: BuyerService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    card = card_service.add(buyer.id, CardCreate(**data))
    # new_data = data.copy()
    new_data = {
        "card_number": "9683282416651254",
        "card_name": "Marta Garcia Gómez",
        "card_exp_date": datetime(2026, 1, 1).date().strftime("%Y-%m-%d"),
        "card_security_num": "123",
    }
    response = client.put(f"/cards/me/{card.id}", json=new_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["card_number"] == new_data["card_number"]
    assert content["card_name"] == new_data["card_name"]
    assert content["card_exp_date"] == new_data["card_exp_date"]
    assert "card_security_num" not in content
    assert "id" in content

    card = card_service.get_by_id(content["id"])
    assert new_data["card_security_num"] == card.card_security_num


def test_update_card_invalid_data(
    client: TestClient,
    card_service: CardService,
    buyer_service: BuyerService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    card = card_service.add(buyer.id, CardCreate(**data))
    new_data = data.copy()
    new_data["card_number"] = "1"  # Invalid card number

    response = client.put(f"/cards/me/{card.id}", json=new_data, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_update_same_card_for_buyer(
    client: TestClient,
    buyer_service: BuyerService,
    card_service: CardService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    data["card_exp_date"] = datetime(2026, 1, 1).date()
    card_service.add(buyer.id, CardCreate(**data))

    card2 = card_service.add(
        buyer.id,
        CardCreate(
            card_number="9683282416651254",
            card_name="Marta Garcia Gomez",
            card_exp_date=datetime(2027, 1, 1).date(),
            card_security_num="123",
        ),
    )

    update_data = {"card_number": data["card_number"]}
    response = client.put(f"/cards/me/{card2.id}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    card_num = data["card_number"]
    assert (
        content["detail"]
        == f"Card with number {card_num} already exists for buyer with id {buyer.id}."
    )


def test_delete_card(
    client: TestClient,
    card_service: CardService,
    buyer_service: BuyerService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_card()
    card = card_service.add(buyer.id, CardCreate(**data))

    response = client.delete(f"/cards/me/{card.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    card = db.execute(select(Card).where(Card.id == card.id)).scalar_one_or_none()
    assert card is None


def test_delete_card_not_found(client: TestClient, buyer_service: BuyerService):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))
    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete("/cards/me/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert (
        content["detail"] == f"Card with id 999 not found for buyer with id {buyer.id}."
    )


def test_delete_cards(
    client: TestClient,
    card_service: CardService,
    buyer_service: BuyerService,
    db: Session,
):
    john = buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
            birth_date="1991-09-09",
            dni="12345678A",
            eco_points=0,
            billing_address="Street Whatever 123",
            payment_method="Bizum",
            password="arandompassword",
        )
    )

    login_data = {"username": john.email, "password": "arandompassword"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    card_service.add(
        john.id,
        CardCreate(
            card_number="5555555555554444",
            card_name="Pedro Fernandez Gómez",
            card_exp_date=datetime(2026, 2, 1).date().strftime("%Y-%m-%d"),
            card_security_num="333",
        ),
    )

    card_service.add(
        john.id,
        CardCreate(
            card_number="0625824103481501",
            card_name="Marta Garcia Gómez",
            card_exp_date=datetime(2025, 1, 1).date().strftime("%Y-%m-%d"),
            card_security_num="123",
        ),
    )
    card_service.add(
        john.id,
        CardCreate(
            card_number="0199322468415426",
            card_name="Mario Perez Martinez",
            card_exp_date=datetime(2027, 9, 1).date().strftime("%Y-%m-%d"),
            card_security_num="193",
        ),
    )

    response = client.delete("/cards/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    cards = db.execute(select(Card).where(Card.id_buyer == john.id)).all()
    assert len(cards) == 0
