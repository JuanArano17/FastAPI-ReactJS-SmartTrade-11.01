from fastapi.testclient import TestClient
from fastapi import status
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
    print(seller_product)
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


