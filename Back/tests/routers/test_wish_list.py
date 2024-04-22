from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.service.product import ProductService
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.in_wish_list import InWishListCreate
from app.schemas.users.types.seller import SellerCreate
from app.schemas.products.seller_product import SellerProductCreate
from app.service.buyer import BuyerService
from app.service.in_wish_list import InWishListService
from app.service.seller import SellerService
from app.service.seller_product import SellerProductService


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


def fake_seller():
    return {
        "email": "donaldtrump@gmail.com",
        "name": "Donald",
        "surname": "Trump",
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
        "eco_points": 10,
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

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    wish_list_item = {"id_seller_product": seller_product.id}

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=wish_list_item)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id_seller_product" in content
    assert content["id_buyer"] == buyer.id
    assert content["id_seller_product"] == seller_product.id

    wish_list_item = wish_list_service.get_by_id(
        content["id_seller_product"], content["id_buyer"]
    )
    assert wish_list_item is not None
    assert content["id_buyer"] == wish_list_item.id_buyer
    assert content["id_seller_product"] == seller_product.id


def test_create_wish_list_invalid_seller_product(
    client: TestClient, buyer_service: BuyerService
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    data = {"id_seller_product": 999}

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=data)
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

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=data)
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

    response = client.get(f"/buyers/{buyer.id}/wish_list/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert wish_list_item.id_seller_product in [
        wish_list["id_seller_product"] for wish_list in content
    ]
    assert wish_list_item.id_buyer in [wish_list["id_buyer"] for wish_list in content]
    assert wish_list_item2.id_seller_product in [
        wish_list["id_seller_product"] for wish_list in content
    ]
    assert wish_list_item2.id_buyer in [wish_list["id_buyer"] for wish_list in content]
    assert wish_list_item3.id_seller_product in [
        wish_list["id_seller_product"] for wish_list in content
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

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    wish_list_item = InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item = wish_list_service.add(buyer.id, wish_list_item=wish_list_item)

    response = client.delete(f"/buyers/{buyer.id}/wish_list/{seller_product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # list_item = db.execute(
    #    select(InWishList).where(InWishList.id == list_item.id)
    # ).scalar_one_or_none()  # type: ignore
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

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    response = client.delete(f"/buyers/{buyer.id}/wish_list/{seller_product.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Seller product with id 999 not found."


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

    response = client.delete(f"/buyers/{buyer.id}/wish_list")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    # wish_list = db.execute(select(InWishList).where(InWishList.id_seller_product == seller_product.id and InWishList.id_buyer == buyer.id)).all()
    # assert len(wish_list) == 0
