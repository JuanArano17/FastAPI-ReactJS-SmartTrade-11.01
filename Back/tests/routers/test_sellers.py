from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users.types.seller import Seller
from app.schemas.users.types.seller import SellerCreate
from app.service.users.types.seller import SellerService
from app.models.users.types.user import User


def fake_seller():
    return {
        "email": "donaldtrump@gmail.com",
        "name": "Donald",
        "surname": "Trump",
        "birth_date": "1992-03-03",
        "bank_data": "Random bank data",
        "cif": "S31002655",
        "password": "randompassword",
    }


def test_create_seller(client: TestClient, seller_service: SellerService, db: Session):
    data = fake_seller()

    response = client.post("/sellers/", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    assert content["name"] == data["name"]
    assert content["surname"] == data["surname"]
    assert content["bank_data"] == data["bank_data"]
    assert content["cif"] == data["cif"]
    assert content["birth_date"] == data["birth_date"]
    assert "id" in content
    assert "password" not in content

    seller = seller_service.get_by_id(content["id"])
    assert seller is not None
    assert seller.password != data["password"]


def test_create_seller_invalid_data(client: TestClient):
    data = fake_seller()
    data["cif"] = "1234"  # Invalid CIF

    response = client.post("/sellers/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_seller_with_used_cif(client: TestClient, db: Session):
    seller = fake_seller()
    db.add(Seller(**seller))
    db.commit()

    seller2 = fake_seller()
    seller2["email"] = "another@gmail.com"
    response = client.post("/sellers/", json=seller2)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == f"Seller with cif {seller['cif']} already exists."


def test_create_seller_with_used_email(client: TestClient, db: Session):
    db.add(
        User(
            email="alreadyinuse@gmail.com",
            name="Fake",
            surname="Fake Fake",
            password="fake",
        )
    )
    db.commit()

    data = fake_seller()
    data["email"] = "alreadyinuse@gmail.com"

    response = client.post("/sellers/", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == f"User with email {data['email']} already exists."


def test_get_seller_by_id(
    client: TestClient, seller_service: SellerService, db: Session
):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    response = client.get(f"/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    assert content["name"] == data["name"]
    assert content["surname"] == data["surname"]
    assert content["bank_data"] == data["bank_data"]
    assert content["cif"] == data["cif"]
    assert content["birth_date"] == data["birth_date"]
    assert "id" in content
    assert "password" not in content
    assert content["id"] == seller.id
    assert seller.password != data["password"]


def test_get_seller_not_found(client: TestClient):
    response = client.get("/sellers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Seller with id 999 not found."


def test_get_sellers(client: TestClient, seller_service: SellerService):
    samuel = seller_service.add(
        SellerCreate(
            email="samuelwinshester@gmail.com",
            name="Samuel",
            surname="Winshester",
            birth_date="1992-03-03",
            bank_data="Random bank data",
            cif="S31002655",
            password="randompassword",
        )
    )

    taylor = seller_service.add(
        SellerCreate(
            email="tayloranderson@gmail.com",
            name="Taylor",
            surname="Anderson",
            birth_date="1992-03-03",
            bank_data="Whatever bank data",
            cif="S31002656",
            password="whateverpass",
        )
    )

    hendrick = seller_service.add(
        SellerCreate(
            email="hendricksousa@hotmail.com",
            name="Hendrick",
            surname="Sousa",
            birth_date="1992-03-03",
            bank_data="Another bank data",
            cif="S31002657",
            password="anotherpass",
        )
    )

    response = client.get("/sellers/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert samuel.id in [seller["id"] for seller in content]
    assert taylor.id in [seller["id"] for seller in content]
    assert hendrick.id in [seller["id"] for seller in content]


# TODO: check update method
def test_update_seller(client: TestClient, seller_service: SellerService):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    new_data = {
        "name": "Donaldnew",
        "surname": "New Trump",
        "bank_data": "New bank data",
        "cif": "S31002657",
        "password": "newpassword",
        "birth_date": "1997-09-09",
    }

    response = client.put(f"/sellers/{seller.id}", json=new_data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["email"] == data["email"]
    assert content["name"] == new_data["name"]
    assert content["surname"] == new_data["surname"]
    assert content["bank_data"] == new_data["bank_data"]
    assert content["cif"] == new_data["cif"]
    assert "id" in content
    assert "password" not in content


# TODO: check update method
def test_update_seller_invalid_data(client: TestClient, seller_service: SellerService):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    new_data = {
        "name": "Donaldnew",
        "surname": "New Trump",
        "bank_data": "New bank data",
        "cif": "1234",
        "password": "newpassword",
    }

    response = client.put(f"/sellers/{seller.id}", json=new_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_update_seller_with_used_cif(
    client: TestClient, seller_service: SellerService, db: Session
):
    seller = fake_seller()
    db.add(Seller(**seller))
    db.commit()

    seller2 = seller_service.add(
        SellerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            birth_date="1992-03-03",
            bank_data="Whatever bank data",
            cif="S31002656",
            password="mypass@123",
        )
    )
    seller_update = {
        "cif": "S31002655",
    }
    response = client.put(f"/sellers/{seller2.id}", json=seller_update)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert (
        content["detail"] == f"Seller with CIF {seller_update['cif']} already exists."
    )


def test_update_seller_with_used_email(
    client: TestClient, seller_service: SellerService, db: Session
):
    seller = fake_seller()
    db.add(Seller(**seller))
    db.commit()

    seller2 = seller_service.add(
        SellerCreate(
            email="mariacarey@hotmail.com",
            name="Maria",
            surname="Carey",
            birth_date="1992-03-03",
            bank_data="Whatever bank data",
            cif="S31002656",
            password="mypass@123",
        )
    )
    seller_update = {
        "email": "donaldtrump@gmail.com",
    }

    response = client.put(f"/sellers/{seller2.id}", json=seller_update)
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert (
        content["detail"] == f"User with email {seller_update['email']} already exists."
    )


def test_delete_seller(client: TestClient, seller_service: SellerService, db: Session):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    response = client.delete(f"/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    seller = db.execute(select(User).where(User.id == seller.id)).scalar_one_or_none()
    assert seller is None


def test_delete_seller_not_found(client: TestClient):
    response = client.delete("/sellers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Seller with id 999 not found."


def test_delete_all_sellers(
    client: TestClient, seller_service: SellerService, db: Session
):
    seller_service.add(
        SellerCreate(
            email="joshuaholtz@gmail.com",
            name="Joshua",
            surname="Holtz",
            birth_date="1992-03-03",
            bank_data="Random bank data",
            cif="S31002655",
            password="randompassword",
        )
    )

    seller_service.add(
        SellerCreate(
            email="jefflombrado@gmail.com",
            name="Jeff",
            surname="Lombrado",
            birth_date="1992-03-03",
            bank_data="Random bank data",
            cif="S31002656",
            password="randompassword",
        )
    )

    seller_service.add(
        SellerCreate(
            email="jessicatrinity@gmail.com",
            name="Jessica",
            surname="Trinity",
            birth_date="1992-03-03",
            bank_data="Random bank data",
            cif="S31002657",
            password="randompassword",
        )
    )

    response = client.delete("/sellers/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    sellers = db.execute(select(User)).all()
    assert len(sellers) == 0
