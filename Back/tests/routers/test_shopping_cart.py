from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.service.products.product import ProductService
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.types.seller import SellerCreate
from app.schemas.products.seller_product import SellerProductCreate, SellerProductUpdate
from app.service.users.types.buyer import BuyerService
from app.service.users.in_shopping_cart import InShoppingCartService
from app.service.users.types.seller import SellerService
from app.service.products.seller_product import SellerProductService
from app.schemas.users.in_shopping_cart import InShoppingCartCreate


def fake_buyer():
    return {
        "email": "mytestemail@gmail.com",
        "name": "Jonathan",
        "surname": "Wick Doe",
        "dni": "58263711F",
        "birth_date": "1992-03-03",
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
        "birth_date": "1992-03-03",
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


def test_create_shopping_cart(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = {"id_seller_product": seller_product.id, "quantity": 2}

    response = client.post(f"/shopping_cart/me", json=shopping_cart_item, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "seller_product" in content
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
    assert "id" in content
    assert content["id_buyer"] == buyer.id
    assert content["quantity"] == shopping_cart_item["quantity"]

    shopping_cart_item = shopping_cart_service.get_by_id(
       content["id"]
    )
    assert shopping_cart_item is not None
    assert content["id_buyer"] == shopping_cart_item.id_buyer
    assert content["quantity"] == shopping_cart_item.quantity

    data = fake_seller_product()
    data["id_product"] = product.id
    data["quantity"] = 1
    seller_product = seller_product_service.update(
        seller_product.id, SellerProductUpdate(**data)
    )

    shopping_cart_item = shopping_cart_service.get_by_id(
        content["id"]
    )
    assert shopping_cart_item is not None
    assert shopping_cart_item.id_buyer == shopping_cart_item.id_buyer
    assert shopping_cart_item.id_seller_product == seller_product.id
    assert shopping_cart_item.quantity == seller_product.quantity


def test_create_shopping_cart_invalid_quantity(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = {"id_seller_product": seller_product.id, "quantity": 10000}

    response = client.post(f"/shopping_cart/me", json=shopping_cart_item, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()


def test_create_shopping_cart_invalid_seller_product(
    client: TestClient, buyer_service: BuyerService
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    login_data = {"username": data["email"], "password": data["password"]}

    login_response = client.post("/login/access-token", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    data = {"id_seller_product": 999, "quantity":1}

    response = client.post(f"/shopping_cart/me", json=data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


def test_create_duplicate_shopping_cart(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = InShoppingCartCreate(
        id_seller_product=seller_product.id, quantity=1
    )
    shopping_cart_item = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item
    )

    data = {"id_seller_product": shopping_cart_item.id_seller_product, "quantity": 1}

    response = client.post(f"/shopping_cart/me", json=data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()


def test_get_shopping_cart(
    client: TestClient,
    db: Session,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product.id
    )
    shopping_cart_item = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item
    )
    shopping_cart_item2 = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product2.id
    )
    shopping_cart_item2 = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item2
    )
    shopping_cart_item3 = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product3.id
    )
    shopping_cart_item3 = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item3
    )

    response = client.get(f"/shopping_cart/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert shopping_cart_item.id_seller_product in [
        shopping_cart["seller_product"]["id"] for shopping_cart in content
    ]
    assert shopping_cart_item.id_buyer in [
        shopping_cart["id_buyer"] for shopping_cart in content
    ]
    assert shopping_cart_item2.id_seller_product in [
        shopping_cart["seller_product"]["id"] for shopping_cart in content
    ]
    assert shopping_cart_item2.id_buyer in [
        shopping_cart["id_buyer"] for shopping_cart in content
    ]
    assert shopping_cart_item3.id_seller_product in [
        shopping_cart["seller_product"]["id"] for shopping_cart in content
    ]
    assert shopping_cart_item3.id_buyer in [
        shopping_cart["id_buyer"] for shopping_cart in content
    ]


def test_delete_shopping_cart_item(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product.id
    )
    shopping_cart_item = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item
    )

    response = client.delete(f"/shopping_cart/me/{shopping_cart_item.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # list_item = db.execute(
    #    select(InWishList).where(InWishList.id == list_item.id)
    # ).scalar_one_or_none()
    # assert list_item is None


def test_delete_shopping_cart_item_not_found(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    response = client.delete(f"/shopping_cart/me/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Cart item with id 999 not found."


def test_delete_shopping_cart(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    shopping_cart_service: InShoppingCartService,
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

    shopping_cart_item = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product.id
    )
    shopping_cart_item = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item
    )
    shopping_cart_item2 = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product2.id
    )
    shopping_cart_item2 = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item2
    )
    shopping_cart_item3 = InShoppingCartCreate(
        quantity=1, id_seller_product=seller_product3.id
    )
    shopping_cart_item3 = shopping_cart_service.add(
        buyer.id, shopping_cart_product=shopping_cart_item3
    )

    response = client.delete(f"/shopping_cart/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # wish_list = db.execute(select(InWishList).where(InWishList.id_seller_product == seller_product.id and InWishList.id_buyer == buyer.id)).all()
    # assert len(wish_list) == 0
