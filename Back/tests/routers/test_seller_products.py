from fastapi.testclient import TestClient
from fastapi import HTTPException, status
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.service.products.product import ProductService
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.types.seller import SellerCreate
from app.schemas.products.seller_product import SellerProductCreate, SellerProductUpdate
from app.service.users.types.buyer import BuyerService
from app.service.users.types.seller import SellerService
from app.service.products.seller_product import SellerProductService


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


def test_create_seller_product (
    client: TestClient,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    db: Session,
):

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    print (data)
    response = client.post(f"/seller_products/?seller_id={seller.id}", json=data)
    print (response)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id" in content
    assert content["id_product"] == product.id
    assert content["id_seller"] == seller.id
    assert content["price"] == data["price"]
    assert content["shipping_costs"] == data["shipping_costs"]
    assert content["quantity"] == data["quantity"]
    assert content["sizes"] == []

    seller_product = seller_product_service.get_by_id_full(
       content["id"]
    )
    assert seller_product is not None
    assert seller_product.id == content["id"] 
    assert seller_product.quantity == content["quantity"]
    assert seller_product.id_product == content["id_product"]
    assert seller_product.id_seller == content["id_seller"] 
    assert seller_product.state == "Pending"
    assert seller_product.description == None
    assert seller_product.justification == None
    assert seller_product.age_restricted == False
    assert seller_product.name == product.name 
    assert seller_product.spec_sheet == product.spec_sheet 
    assert seller_product.eco_points == 0
    assert seller_product.stock == product.stock 
    assert seller_product.author == product.author
    assert seller_product.pages == product.pages
    assert seller_product.category == product.category
    assert seller_product.images == product.images
    assert seller_product.price == data["price"]
    assert seller_product.shipping_costs == data["shipping_costs"]
    assert seller_product.quantity == data["quantity"] 
    assert seller_product.sizes == None

def test_create_seller_product_invalid_data(
    client: TestClient,
    product_service: ProductService,
    seller_service: SellerService,
    db: Session,
):

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    data["quantity"] = -1

    response = client.post(f"/seller_products/?seller_id={seller.id}", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_create_seller_product_invalid_product(
    client: TestClient, seller_service: SellerService,
):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))
    data = fake_seller_product()
    data["id_product"] = 999
    response = client.post(f"/seller_products/?seller_id={seller.id}", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()

def test_create_duplicate_seller_product(
    client: TestClient,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
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

    response = client.post(f"/seller_products/?seller_id={seller.id}", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "detail" in response.json()
    
def test_get_seller_product(
    client: TestClient,
    db: Session,
    buyer_service: BuyerService,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))

    response = client.get(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    assert content["id"] == seller_product.id
    assert content["quantity"] == seller_product.quantity
    assert content["id_product"] == seller_product.id_product
    assert content["id_seller"] == seller_product.id_seller
    assert content["state"] == "Pending"
    assert "description" not in content
    assert "justification" not in content
    assert content["age_restricted"] == False
    assert content["name"] == product.name 
    assert content["spec_sheet"] == product.spec_sheet 
    assert content["eco_points"] == 0
    assert content["stock"] == product.stock 
    assert content["author"] == product.author
    assert content["pages"] == product.pages
    assert content["category"] == product.category
    assert content["images"] == product.images
    assert content["price"] == data["price"]
    assert content["shipping_costs"] == data["shipping_costs"]
    assert content["quantity"] == data["quantity"] 
    assert "sizes" not in content

def test_get_approved_seller_products(
    client: TestClient,
    db: Session,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_book()
    data["name"] = "Book2"
    product2 = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data["cif"] = "H31002655"
    data["email"] = "lucas@gmail.com"

    seller2 = seller_service.add(SellerCreate(**data))

    data["cif"] = "F31002655"
    data["email"] = "victor@gmail.com"

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))
    data={"state": "Approved", "eco_points": 99, "age_restricted": False}
    seller_product = seller_product_service.update(seller_product.id, SellerProductUpdate(**data))

    data = fake_seller_product()
    data["id_product"] = product2.id
    seller_product2 = seller_product_service.add(
        seller2.id, SellerProductCreate(**data)
    )
    data={"state": "Approved", "eco_points": 69, "age_restricted": True}
    seller_product2 = seller_product_service.update(seller_product2.id, SellerProductUpdate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product3 = seller_product_service.add(
        seller2.id, SellerProductCreate(**data)
    )
    data={"state": "Approved", "eco_points": 79, "age_restricted": True}
    seller_product3 = seller_product_service.update(seller_product3.id, SellerProductUpdate(**data))
    response = client.get(f"/seller_products/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    
    assert len(content) == 3
    assert seller_product.id in [
        seller_product["id"] for seller_product in content
    ]
    assert seller_product2.id in [
        shopping_cart["id"] for shopping_cart in content
    ]
    assert seller_product3.id in [
        shopping_cart["id"] for shopping_cart in content
    ]

def test_approve_seller_product(
    client: TestClient,
    db: Session,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))
    data={"state": "Approved", "eco_points": 99, "age_restricted": True}
    seller_product = seller_product_service.update(seller_product.id, SellerProductUpdate(**data))

    response = client.get(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == seller_product.id
    assert content["quantity"] == seller_product.quantity
    assert content["id_product"] == seller_product.id_product
    assert content["id_seller"] == seller_product.id_seller
    assert content["state"] == "Approved"
    assert "description" not in content
    assert content["justification"] == ""
    assert content["age_restricted"] == True
    assert content["name"] == product.name 
    assert content["spec_sheet"] == product.spec_sheet 
    assert content["eco_points"] == 99
    assert content["stock"] == product.stock 
    assert content["author"] == product.author
    assert content["pages"] == product.pages
    assert content["category"] == product.category
    assert content["images"] == product.images
    assert content["price"] == seller_product.price
    assert content["shipping_costs"] == seller_product.shipping_costs
    assert content["quantity"] == seller_product.quantity
    assert "sizes" not in content

def test_approve_seller_product_missing_eco_points(
    client: TestClient,
    db: Session,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))
    data={"state": "Approved", "age_restricted": True}
    seller_product = seller_product_service.update(seller_product.id, SellerProductUpdate(**data))

    response = client.get(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_approve_seller_product_missing_age_restricted(
    client: TestClient,
    db: Session,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))
    data={"state": "Approved", "eco_points": 99}
    seller_product = seller_product_service.update(seller_product.id, SellerProductUpdate(**data))

    response = client.get(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_reject_seller_product(
    client: TestClient,
    db: Session,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService
):
    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller()
    seller1 = seller_service.add(SellerCreate(**data))

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller1.id, SellerProductCreate(**data))
    data={"state": "Rejected", "justification": "yes"}
    seller_product = seller_product_service.update(seller_product.id, SellerProductUpdate(**data))

    response = client.get(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["id"] == seller_product.id
    assert content["quantity"] == seller_product.quantity
    assert content["id_product"] == seller_product.id_product
    assert content["id_seller"] == seller_product.id_seller
    assert content["state"] == "Rejected"
    assert "description" not in content
    assert content["justification"] == data["justification"]
    assert content["age_restricted"] == False
    assert content["name"] == product.name 
    assert content["spec_sheet"] == product.spec_sheet 
    assert content["eco_points"] == 0
    assert content["stock"] == product.stock 
    assert content["author"] == product.author
    assert content["pages"] == product.pages
    assert content["category"] == product.category
    assert content["images"] == product.images
    assert content["price"] == seller_product.price
    assert content["shipping_costs"] == seller_product.shipping_costs
    assert content["quantity"] == seller_product.quantity
    assert "sizes" not in content

def test_delete_seller_product(
    client: TestClient,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    db: Session,
):
    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    response = client.delete(f"/seller_products/{seller_product.id}")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    seller_product1 = client.get(f"/seller_products/{seller_product.id}")
    assert seller_product1.status_code == status.HTTP_404_NOT_FOUND

def test_delete_seller_product_not_found(
    client: TestClient,
    product_service: ProductService,
    seller_service: SellerService,
    seller_product_service: SellerProductService,
):

    data = fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data = fake_book()
    product = product_service.add("book", data)

    data = fake_seller_product()
    data["id_product"] = product.id
    seller_product = seller_product_service.add(seller.id, SellerProductCreate(**data))

    response = client.delete(f"/seller_products/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Seller product with id 999 not found."

