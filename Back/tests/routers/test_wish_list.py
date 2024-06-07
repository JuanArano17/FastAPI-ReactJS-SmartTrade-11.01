from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.service.products.product import ProductService
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.in_wish_list import InWishListCreate
from app.schemas.users.types.seller import SellerCreate
from app.schemas.products.seller_product import SellerProductCreate
from app.service.users.types.buyer import BuyerService
from app.service.users.in_wish_list import InWishListService
from app.service.users.types.seller import SellerService
from app.service.products.seller_product import SellerProductService


def fake_buyer():
    return {
        "email": "mytestemail@gmail.com",
        "name": "Jonathan",
        "surname": "Wick Doe",
        "birth_date": "1992-03-08",
        "dni": "58263711F",
        "eco_points": 0,
        "billing_address": "Street Whatever 123",
        "payment_method": "Bizum",
        "password": "arandompassword",
    }


def fake_seller():
    return {
        "email": "donaldtrump@gmail.com",
        "name": "Donald",
        "surname": "Trump",
        "birth_date": "1999-03-03",
        "bank_data": "Random bank data",
        "cif": "S31002655",
        "password": "randompassword",
    }


def fake_book():
    return {
        "name": "Dune",
        "description": None,
        "spec_sheet": "Specs...",
        "stock": 0,
        "author": "Frank Herbert",
        "pages": 900,
    }


def fake_seller_product():
    return {
        "quantity": 3,
        "price": 1,
        "shipping_costs": 1,
    }


def test_create_wish_list(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    wish_list_item = {"id_seller_product": seller_product.id}

    response = client.post(f"/wish_list/me", json=wish_list_item, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "seller_product" in content
    assert content["id_buyer"] == buyer.id
    assert content["seller_product"]["id"] == seller_product.id
    assert content["seller_product"]["id_product"] == product.id
    assert content["seller_product"]["id_seller"] == seller.id
    assert content["seller_product"]["state"] == "Pending"
    assert "description" not in content["seller_product"]
    assert "justification" not in content["seller_product"]
    assert content["seller_product"]["age_restricted"] == seller_product.age_restricted
    assert content["seller_product"]["name"] == product.name
    assert content["seller_product"]["spec_sheet"] == product.spec_sheet
    assert content["seller_product"]["eco_points"] == seller_product.eco_points
    assert content["seller_product"]["stock"] == product.stock
    assert content["seller_product"]["author"] == product.author
    assert content["seller_product"]["pages"] == product.pages
    assert content["seller_product"]["category"] == product.category
    assert content["seller_product"]["images"] == product.images
    assert content["seller_product"]["price"] == seller_product.price
    assert content["seller_product"]["shipping_costs"] == seller_product.shipping_costs
    assert content["seller_product"]["quantity"] == seller_product.quantity

    wish_list_item = wish_list_service.get_by_id(
        content["seller_product"]["id"], content["id_buyer"]
    )
    assert wish_list_item is not None
    assert content["id_buyer"] == wish_list_item.id_buyer
    #assert content["id_seller_product"] == seller_product.id


def test_create_wish_list_invalid_seller_product(
    client: TestClient, buyer_service: BuyerService
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = {"id_seller_product": 999}

    response = client.post(f"/wish_list/me", json=data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


def test_create_duplicate_wish_list(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    wish_list_item = InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item = wish_list_service.add(buyer.id, wish_list_item=wish_list_item)

    data = {"id_seller_product": wish_list_item.id_seller_product}

    response = client.post(f"/wish_list/me", json=data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()


def test_get_wish_list(
    client: TestClient,
    db: Session,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_book()
    data["name"] = "Book2"
    product2 = product_service.add("book", data)

    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data["cif"] = "H31002655"
    data["email"] = "lucas@gmail.com"

    seller2 = seller_service.add(SellerCreate(**data))

    data["cif"] = "F31002655"
    data["email"] = "victor@gmail.com"

    seller3 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product2.id
    seller_product2 = seller_product_service.add(
        seller2.id, SellerProductCreate(**data)
    )

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product3 = seller_product_service.add(
        seller3.id, SellerProductCreate(**data)
    )

    wish_list_item = InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item = wish_list_service.add(buyer.id, wish_list_item=wish_list_item)
    wish_list_item2 = InWishListCreate(id_seller_product=seller_product2.id)
    wish_list_item2 = wish_list_service.add(buyer.id, wish_list_item=wish_list_item2)
    wish_list_item3 = InWishListCreate(id_seller_product=seller_product3.id)
    wish_list_item3 = wish_list_service.add(buyer.id, wish_list_item=wish_list_item3)

    response = client.get(f"/wish_list/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert wish_list_item.id_seller_product in [
        wish_list["seller_product"]["id"] for wish_list in content
    ]
    assert wish_list_item.id_buyer in [wish_list["id_buyer"] for wish_list in content]
    assert wish_list_item2.id_seller_product in [
        wish_list["seller_product"]["id"] for wish_list in content
    ]
    assert wish_list_item2.id_buyer in [wish_list["id_buyer"] for wish_list in content]
    assert wish_list_item3.id_seller_product in [
        wish_list["seller_product"]["id"] for wish_list in content
    ]
    assert wish_list_item3.id_buyer in [wish_list["id_buyer"] for wish_list in content]


def test_delete_wish_list_item(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
    db: Session,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}    

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    wish_list_item = InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item = wish_list_service.add(buyer.id, wish_list_item=wish_list_item)

    response = client.delete(f"/wish_list/me/{seller_product.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # list_item = db.execute(
    #    select(InWishList).where(InWishList.id == list_item.id)
    # ).scalar_one_or_none()
    # assert list_item is None


def test_delete_wish_list_item_not_found(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    response = client.delete(f"/wish_list/me/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Wishlist item not found"


def test_delete_wish_list(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
    db: Session,
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_book()
    data["name"] = "Book2"
    product2 = product_service.add("book", data)

    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data["cif"] = "H31002655"
    data["email"] = "lucas@gmail.com"

    seller2 = seller_service.add(SellerCreate(**data))

    data["cif"] = "F31002655"
    data["email"] = "victor@gmail.com"

    seller3 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product2.id
    seller_product2 = seller_product_service.add(
        seller2.id, SellerProductCreate(**data)
    )

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product3 = seller_product_service.add(
        seller3.id, SellerProductCreate(**data)
    )

    wish_list_item = InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item = wish_list_service.add(buyer.id, wish_list_item=wish_list_item)
    wish_list_item2 = InWishListCreate(id_seller_product=seller_product2.id)
    wish_list_item2 = wish_list_service.add(buyer.id, wish_list_item=wish_list_item2)
    wish_list_item3 = InWishListCreate(id_seller_product=seller_product3.id)
    wish_list_item3 = wish_list_service.add(buyer.id, wish_list_item=wish_list_item3)

    response = client.delete(f"/wish_list/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # wish_list = db.execute(select(InWishList).where(InWishList.id_seller_product == seller_product.id and InWishList.id_buyer == buyer.id)).all()
    # assert len(wish_list) == 0
