from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users.types.user import User
from app.schemas.users.types.buyer import BuyerCreate
from app.models.users.types.buyer import Buyer
from app.service.buyer import BuyerService


def fake_buyer():
    return {
        "email": "mytestemail@gmail.com",
        "name": "Jonathan",
        "surname": "Wick Doe",
        "dni": "58263711F",
        "eco_points": 0,
        "billing_address": "Street Whatever 123",
        "payment_method": "Bizum",
        "password": "arandompassword",
    }


def test_create_buyer(client: TestClient, buyer_service: BuyerService, db: Session):
    data = fake_buyer()

    response = client.post("/buyers/", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    assert content["name"] == data["name"]
    assert content["surname"] == data["surname"]
    assert content["dni"] == data["dni"]
    assert content["billing_address"] == data["billing_address"]
    assert content["payment_method"] == data["payment_method"]
    assert "id" in content
    assert "password" not in content

    buyer = buyer_service.get_by_id(content["id"])
    assert buyer is not None
    assert buyer.password != data["password"]  # type: ignore


def test_create_buyer_invalid_data(client: TestClient):
    data = fake_buyer()
    data["dni"] = "1234"  # Invalid DNI

    response = client.post("/buyers/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_buyer_with_used_dni(client: TestClient, db: Session):
    buyer = fake_buyer()
    db.add(Buyer(**buyer))
    db.commit()

    buyer2 = fake_buyer()
    buyer2["email"] = "example@example.com"
    response = client.post("/buyers/", json=buyer2)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == f"Buyer with dni {buyer['dni']} already exists."


def test_create_buyer_with_used_email(client: TestClient, db: Session):
    db.add(
        User(
            email="alreadyinuse@gmail.com",
            name="Fake",
            surname="Fake Fake",
            password="fake",
        )
    )
    db.commit()

    data = fake_buyer()
    data["email"] = "alreadyinuse@gmail.com"

    response = client.post("/buyers/", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == f"User with email {data['email']} already exists."


def test_get_buyer_by_id(client: TestClient, buyer_service: BuyerService, db: Session):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    response = client.get(f"/buyers/{buyer.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    assert content["name"] == data["name"]
    assert content["surname"] == data["surname"]
    assert content["dni"] == data["dni"]
    assert content["billing_address"] == data["billing_address"]
    assert content["payment_method"] == data["payment_method"]
    assert "id" in content
    assert "password" not in content
    assert content["id"] == buyer.id  # type: ignore
    assert buyer.password != data["password"]  # type: ignore


def test_get_buyer_not_found(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    response = client.get("/buyers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Buyer with id 999 not found."


def test_get_buyers(client: TestClient, buyer_service: BuyerService, db: Session):
    john = buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
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
            dni="87654321B",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )
    dean = buyer_service.add(
        BuyerCreate(
            email="deanwinshester@gmail.com",
            name="Dean",
            surname="Winshester",
            dni="12348765C",
            eco_points=0,
            billing_address="Street Winshesters 912",
            payment_method="Bizum",
            password="castiel456",
        )
    )

    response = client.get("/buyers/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert john.id in [buyer["id"] for buyer in content]
    assert maria.id in [buyer["id"] for buyer in content]
    assert dean.id in [buyer["id"] for buyer in content]


# TODO: review update method
def test_update_buyer(client: TestClient, buyer_service: BuyerService, db: Session):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    # new_data = data.copy()
    new_data = {
        "dni": "12345678Z",
        "eco_points": 100,
        "billing_address": "New Street 123",
        "payment_method": "Credit Card",
    }
    # new_data["name"] = "New Name"
    # new_data["surname"] = "New Surname"
    # new_data["dni"] = "12345678Z"
    # new_data["eco_points"] = 100
    # new_data["billing_address"] = "New Street 123"
    # new_data["payment_method"] = "Credit Card"

    response = client.put(f"/buyers/{buyer.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    # assert content["name"] == new_data["name"]
    # assert content["surname"] == new_data["surname"]
    assert content["dni"] == new_data["dni"]
    assert content["eco_points"] == new_data["eco_points"]
    assert content["billing_address"] == new_data["billing_address"]
    assert content["payment_method"] == new_data["payment_method"]
    assert "id" in content
    assert "password" not in content


def test_update_buyer_invalid_data(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    new_data = data.copy()
    new_data["name"] = "New Name"
    new_data["surname"] = "New Surname"
    new_data["dni"] = "123"  # Invalid DNI
    new_data["eco_points"] = 100
    new_data["billing_address"] = "New Street 123"
    new_data["payment_method"] = "Credit Card"

    response = client.put(f"/buyers/{buyer.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_update_buyer_with_used_dni(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    buyer = fake_buyer()
    db.add(Buyer(**buyer))
    db.commit()

    buyer2 = buyer_service.add(
        BuyerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            dni="87654321B",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )
    buyer_update = {
        "dni": "58263711F",
    }
    response = client.put(f"/buyers/{buyer2.id}", json=buyer_update)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == f"Buyer with dni {buyer_update['dni']} already exists."


def test_update_buyer_with_used_email(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    buyer = fake_buyer()
    db.add(Buyer(**buyer))
    db.commit()

    buyer2 = buyer_service.add(
        BuyerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            dni="87654321B",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )
    buyer_update = {
        "email": buyer["email"],
    }
    response = client.put(f"/buyers/{buyer2.id}", json=buyer_update)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert (
        content["detail"] == f"User with email {buyer_update['email']} already exists."
    )


def test_delete_buyer(client: TestClient, buyer_service: BuyerService, db: Session):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    response = client.delete(f"/buyers/{buyer.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    buyer = db.execute(select(User).where(User.id == buyer.id)).scalar_one_or_none()  # type: ignore
    assert buyer is None


def test_delete_buyer_not_found(client: TestClient):
    response = client.delete("/buyers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Buyer with id 999 not found."


def test_delete_buyers(client: TestClient, buyer_service: BuyerService, db: Session):
    buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
            dni="12345678A",
            eco_points=0,
            billing_address="Street Whatever 123",
            payment_method="Bizum",
            password="arandompassword",
        )
    )
    buyer_service.add(
        BuyerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            dni="87654321B",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )
    buyer_service.add(
        BuyerCreate(
            email="deanwinshester@gmail.com",
            name="Dean",
            surname="Winshester",
            dni="12348765C",
            eco_points=0,
            billing_address="Street Winshesters 912",
            payment_method="Bizum",
            password="castiel456",
        )
    )

    response = client.delete("/buyers/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    buyers = db.execute(select(User)).all()
    assert len(buyers) == 0
