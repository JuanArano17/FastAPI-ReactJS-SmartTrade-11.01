from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.image import ImageCreate
from app.models.image import Image
from app.service.image import ImageService
from app.schemas.product import ProductCreate
from app.service.product import ProductService
from schemas.book import BookCreate
from schemas.buyer import BuyerCreate
from schemas.in_wish_list import InWishListCreate
from schemas.seller import SellerCreate
from service.buyer import BuyerService
from service.in_wish_list import InWishListService
from service.seller import SellerService
from service.seller_product import SellerProductService

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
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
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
    db: Session
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))
    
    data=fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data=fake_book()
    product = product_service.add(BookCreate(**data))

    data=fake_seller_product()
    seller_pro = seller_product_service.add(seller.id)

    seller_product=seller_product_service.add(seller.id, seller_product=seller_pro)

    wish_list_item = {"id_seller_product": seller_product.id}

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=wish_list_item)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert "id" in content
    assert "id_seller_product" in content
    assert content["id_buyer"] == buyer.id
    assert content["id_seller_product"] == seller_product.id

    wish_list_item = wish_list_service.get_by_id(content["id"])
    assert wish_list_item is not None
    assert content["id_buyer"] == wish_list_item.id_buyer


def test_create_wish_list_invalid_seller_product(client: TestClient, buyer_service: BuyerService):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    data =  {"id_seller_product":999}

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()

def test_create_duplicate_wish_list(client: TestClient, buyer_service: BuyerService, product_service: ProductService, seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,):

    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))
    
    data=fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data=fake_book()
    product = product_service.add(BookCreate(**data))

    data=fake_seller_product()
    seller_pro = seller_product_service.add(seller.id)

    seller_product=seller_product_service.add(seller.id, seller_product=seller_pro)
    
    wish_list_item=InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item=wish_list_service.add(buyer.id, wish_list_item=wish_list_item)

    data =  {"id_seller_product":wish_list_item.id_seller_product}

    response = client.post(f"/buyers/{buyer.id}/wish_list", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()


def test_get_wish_list_item(
    client: TestClient,
    product_service:ProductService,
    db: Session,
    buyer_service: BuyerService, 
    seller_service: SellerService,
    seller_product_service: SellerProductService,
    wish_list_service: InWishListService,
):
    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))

    data = fake_buyer()
    buyer = buyer_service.add(BuyerCreate(**data))
    
    data=fake_seller()
    seller = seller_service.add(SellerCreate(**data))

    data=fake_book()
    product = product_service.add(BookCreate(**data))

    data=fake_seller_product()
    seller_pro = seller_product_service.add(seller.id)

    seller_product=seller_product_service.add(seller.id, seller_product=seller_pro)
    
    wish_list_item=InWishListCreate(id_seller_product=seller_product.id)
    wish_list_item=wish_list_service.add(buyer.id, wish_list_item=wish_list_item)

    response = client.get(f"/products/{product.id}/images/{image.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["url"] == data["url"]
    assert "id" in content
    assert "id_product" in content
    assert content["id"] == image.id  # type: ignore
    assert content["id_product"] == image.id_product  # type: ignore


def test_get_image_not_found(
    client: TestClient, product_service: ProductService, db: Session
):
    data = fake_product()
    product = product_service.add("book", data)

    response = client.get(f"/products/{product.id}/images/999")  # type: ignore
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Image with id 999 not found."


def test_get_images(
    client: TestClient,
    product_service: ProductService,
    image_service: ImageService,
    db: Session,
):
    book = product_service.add("book",
            {
        "name": "Dune",
        "spec_sheet": "Specs...",
        "eco_points": 10,
        "author": "Frank Herbert",
        "pages": 900,
            }
    )
    game = product_service.add("game",
        {
        "name": "gta6",
        "spec_sheet": "Specs...",
        "eco_points": 10,
        "publisher": "Rockstar",
        "platform": "ps5",
        "size":"100GB",
    }
    )

    image1 = image_service.add(
        book.id,
        ImageCreate(
            url ="https://dummyimage.com/780x968"
        ),
    )

    image2 = image_service.add(
        book.id,
        ImageCreate(
            url ="https://dummyimage2.com/800x968"
        ),
    )
    image3 = image_service.add(
        game.id,
        ImageCreate(
            url ="https://dummyimage3.com/800x968"
        ),
    )

    response = client.get(f"/products/{game.id}/images/")
    response1 = client.get(f"/products/{book.id}/images/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert image3.id in [image["id"] for image in content]
    assert response1.status_code == status.HTTP_200_OK
    content = response1.json()
    assert len(content) == 2
    assert image1.id in [image["id"] for image in content]
    assert image2.id in [image["id"] for image in content]


def test_update_image(
    client: TestClient,
    image_service: ImageService,
    product_service: ProductService,
    db: Session,
):
    data = fake_product()
    product = product_service.add("book",data)

    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))
    # new_data = data.copy()
    new_data = {
        "url":"https://dummyimage2.com/800x968"
    }
    response = client.put(f"/products/{product.id}/images/{image.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["url"] == new_data["url"]
    assert "id" in content
    assert "id_product" in content
    assert content["id_product"] == product.id

def test_update_image_invalid_data(
    client: TestClient,
    image_service: ImageService,
    product_service: ProductService,
    db: Session,
):
    data = fake_product()
    product = product_service.add("book",data)

    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))
    new_data = data.copy()
    new_data["ur"] = "e"  # Wrong field
    response = client.put(f"/products/{product.id}/images/{image.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_delete_image(
    client: TestClient,
    image_service: ImageService,
    product_service: ProductService,
    db: Session,
):
    data = fake_product()
    product = product_service.add("book",data)
    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))

    response = client.delete(f"/products/{product.id}/images/{image.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    image = db.execute(
        select(Image).where(Image.id == image.id)
    ).scalar_one_or_none()  # type: ignore
    assert image is None


def test_delete_image_not_found(client: TestClient, product_service: ProductService):
    data = fake_product()
    product = product_service.add("book",data)
    response = client.delete(f"/products/{product.id}/images/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Image with id 999 not found."


def test_delete_images(
    client: TestClient,
    image_service: ImageService,
    product_service: ProductService,
    db: Session,
):
    book = product_service.add("book",
            {
        "name": "Dune",
        "spec_sheet": "Specs...",
        "eco_points": 10,
        "author": "Frank Herbert",
        "pages": 900,
            }
    )

    image1 = image_service.add(
        book.id,
        ImageCreate(
            url ="https://dummyimage.com/780x968"
        ),
    )

    image2 = image_service.add(
        book.id,
        ImageCreate(
            url ="https://dummyimage2.com/800x968"
        ),
    )
    image3 = image_service.add(
        book.id,
        ImageCreate(
            url ="https://dummyimage3.com/800x968"
        ),
    )

    response = client.delete(f"/products/{book.id}/images")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    cards = db.execute(select(Image).where(Image.id_product == book.id)).all()
    assert len(cards) == 0