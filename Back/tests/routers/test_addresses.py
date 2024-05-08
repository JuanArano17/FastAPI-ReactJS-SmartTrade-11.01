from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.users.address import AddressCreate
from app.models.users.address import Address
from app.service.users.address import AddressService
from app.schemas.users.types.buyer import BuyerCreate
from app.service.users.types.buyer import BuyerService


def fake_address():
    return { 
        "street": "Test Street",
        "floor": 3,
        "door": "A",
        "adit_info": "Cuidado con el perro",
        "city": "Madrid",
        "postal_code": "43211",
        "country": "ESP",
        "default": True
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


def test_create_address(
    client: TestClient,
    buyer_service: BuyerService,
    address_service: AddressService,
    db: Session,
):
    data = fake_buyer()
    buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    data = fake_address()
    response = client.post("/addresses", json=data, headers=headers)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK

    assert content["street"] == data["street"]
    assert content["floor"] == data["floor"]
    assert content["door"] == data["door"]
    assert content["adit_info"] == data["adit_info"]
    assert content["city"] == data["city"]
    assert content["postal_code"] == data["postal_code"]
    assert content["country"] == data["country"]
    assert content["default"] == data["default"]
    assert "id" in content
    assert "id_buyer" in content

    address = address_service.get_by_id(content["id"])
    assert address is not None
    assert address.id_buyer == content["id_buyer"]


def test_create_address_invalid_data(client: TestClient, buyer_service: BuyerService):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_address()
    data["postal_code"] = "fiwofwniewnfw"  # Invalid zip code format

    response = client.post(f"/addresses", json=data, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_default_address_change(
    client: TestClient,
    db: Session,
    address_service: AddressService,
    buyer_service: BuyerService,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))

    address2 = fake_address()
    address2["default"] = True
    response = client.post(f"/addresses", json=address2, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content1 = response.json()
    assert content1["default"] == True
    response = client.get(f"/addresses/{address.id}", headers=headers)
    content = response.json()
    assert content["default"] == False
    address3 = fake_address()
    address3["default"] = True
    response = client.post(f"/addresses", json=address3, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["default"] == True
    response = client.get(f"addresses/{address.id}", headers=headers)
    content = response.json()
    assert content["default"] == False
    address2_id = content1["id"]
    response = client.get(f"/addresses/{address2_id}", headers=headers)
    content = response.json()
    assert content["default"] == False


def test_get_address_by_id(
    client: TestClient,
    address_service: AddressService,
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

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))

    response = client.get(f"/addresses/{address.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["street"] == data["street"]
    assert content["floor"] == data["floor"]
    assert content["door"] == data["door"]
    assert content["adit_info"] == data["adit_info"]
    assert content["city"] == data["city"]
    assert content["postal_code"] == data["postal_code"]
    assert content["country"] == data["country"]
    assert content["default"] == data["default"]
    assert "id" in content
    assert "id_buyer" in content
    assert content["id"] == address.id
    assert content["id_buyer"] == address.id_buyer


def test_get_address_not_found(
    client: TestClient, buyer_service: BuyerService, db: Session
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}


    response = client.get(f"/addresses/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Address with id 999 not found."


def test_get_addresses(
    client: TestClient,
    buyer_service: BuyerService,
    address_service: AddressService,
    db: Session,
):
    john = buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
            dni="12345678A",
            birth_date = "1993-02-02",
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
            birth_date = "1993-02-02",
            eco_points=0,
            billing_address="Street Molotia 2",
            payment_method="Bizum",
            password="mypass@123",
        )
    )

    address1 = address_service.add(
        john.id,
        AddressCreate(
            street="Test Street",
            floor=3,
            adit_info="Cuidado con el perro",
            door="A",
            city="Madrid",
            postal_code="43211",
            country="ESP",
            default=True,
        ),
    )

    address2 = address_service.add(
        john.id,
        AddressCreate(
            street="Main Street",
            floor=1,
            door="C",
            adit_info=None,
            city="Vancouver",
            postal_code="41111",
            country="CAN",
            default=True,
        ),
    )
    address3 = address_service.add(
        maria.id,
        AddressCreate(
            street="Side Street",
            floor=1,
            door="D",
            adit_info=None,
            city="San Francisco",
            postal_code="32222",
            country="USA",
            default=False,
        ),
    )

    login_data = {"username": maria.email, "password": "mypass@123"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/addresses/", headers=headers)

    login_data = {"username": john.email, "password": "arandompassword"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response1 = client.get(f"/addresses/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert address3.id in [address["id"] for address in content]
    assert response1.status_code == status.HTTP_200_OK
    content = response1.json()
    assert len(content) == 2
    assert address1.id in [address["id"] for address in content]
    assert address2.id in [address["id"] for address in content]


def test_update_address(
    client: TestClient,
    address_service: AddressService,
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

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))
    # new_data = data.copy()
    new_data = {
        "street": "Side Street",
        "floor": 9,
        "door": "V",
        "adit_info": "Cuidado con el gato",
        "city": "Ontario",
        "postal_code": "40011",
        "country": "CAN",
        "default": False,
    }
    response = client.put(f"/addresses/{address.id}", json=new_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["street"] == new_data["street"]
    assert content["floor"] == new_data["floor"]
    assert content["door"] == new_data["door"]
    assert content["adit_info"] == new_data["adit_info"]
    assert content["city"] == new_data["city"]
    assert content["postal_code"] == new_data["postal_code"]
    assert content["country"] == new_data["country"]
    assert content["default"] == new_data["default"]
    assert "id" in content


def test_update_default(
    client: TestClient,
    address_service: AddressService,
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

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))

    address2 = address_service.add(
        buyer.id,
        AddressCreate(
            street="Side Street",
            floor=2,
            door="D",
            adit_info=None,
            city="San Francisco",
            postal_code="32222",
            country="USA",
            default=False,
        ),
    )

    # new_data = data.copy()
    new_data = {
        "default": True,
    }

    response = client.put(f"/addresses/{address2.id}", json=new_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["default"] == True

    response = client.get(f"/addresses/{address.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["default"] == False


def test_update_address_invalid_data(
    client: TestClient,
    address_service: AddressService,
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

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))
    new_data = data.copy()
    new_data["postal_code"] = "fiwofwniewnfw"  # Invalid zip code format

    response = client.put(f"/addresses/{address.id}", json=new_data, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_delete_address(
    client: TestClient,
    address_service: AddressService,
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

    data = fake_address()
    address = address_service.add(buyer.id, AddressCreate(**data))

    response = client.delete(f"/addresses/{address.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    address = db.execute(
        select(Address).where(Address.id == address.id)
    ).scalar_one_or_none()
    assert address is None


def test_delete_address_not_found(client: TestClient, buyer_service: BuyerService):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/addresses/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Address with id 999 not found."


def test_delete_addresses(
    client: TestClient,
    address_service: AddressService,
    buyer_service: BuyerService,
    db: Session,
):
    john = buyer_service.add(
        BuyerCreate(
            email="johnwepkins@gmail.com",
            name="John",
            surname="Wepkins",
            dni="12345678A",
            birth_date = "1993-02-02",
            eco_points=0,
            billing_address="Street Whatever 123",
            payment_method="Bizum",
            password="arandompassword",
        )
    )

    address_service.add(
        john.id,
        AddressCreate(
            street="Test Street",
            floor=3,
            door="A",
            adit_info="Cuidado con el perro",
            city="Madrid",
            postal_code="43211",
            country="ESP",
            default=True,
        ),
    )
    address_service.add(
        john.id,
        AddressCreate(
            street="Main Street",
            floor=1,
            door="C",
            adit_info=None,
            city="Vancouver",
            postal_code="41111",
            country="CAN",
            default=True,
        ),
    )
    address_service.add(
        john.id,
        AddressCreate(
            street="Side Street",
            floor=1,
            door="D",
            adit_info=None,
            city="San Francisco",
            postal_code="32222",
            country="USA",
            default=False,
        ),
    )

    login_data = {"username": john.email, "password": "arandompassword"}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/addresses", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    cards = db.execute(select(Address).where(Address.id_buyer == john.id)).all()
    assert len(cards) == 0
