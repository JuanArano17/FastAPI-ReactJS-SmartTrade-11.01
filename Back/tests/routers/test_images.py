from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.products.image import ImageCreate
from app.models.products.image import Image
from app.service.products.image import ImageService
from app.service.products.product import ProductService


def fake_image():
    return {
        "url": "https://dummyimage.com/780x968",
    }


def fake_product():
    return {
        "name": "Dune",
        "spec_sheet": "Specs...",
        "author": "Frank Herbert",
        "pages": 900,
    }


def test_create_image(
    client: TestClient,
    product_service: ProductService,
    image_service: ImageService,
    db: Session,
):
    data = fake_product()
    product = product_service.add("book", data)

    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))

    response = client.post(f"/products/{product.id}/images", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["url"] == data["url"]
    assert "id" in content
    assert "id_product" in content

    image = image_service.get_by_id(content["id"])
    assert image is not None
    assert image.id_product == content["id_product"]


def test_create_image_invalid_data(client: TestClient, product_service: ProductService):
    data = fake_product()
    product = product_service.add("book", data)

    data = {"name": "e"}  # Invalid field

    response = client.post(f"/products/{product.id}/images", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_get_image_by_id(
    client: TestClient,
    image_service: ImageService,
    product_service: ProductService,
    db: Session,
):
    data = fake_product()
    product = product_service.add("book", data)

    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))

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
    book = product_service.add(
        "book",
        {
            "name": "Dune",
            "spec_sheet": "Specs...",
            "author": "Frank Herbert",
            "pages": 900,
        },
    )
    game = product_service.add(
        "game",
        {
            "name": "gta6",
            "spec_sheet": "Specs...",
            "publisher": "Rockstar",
            "platform": "ps5",
            "size": "100GB",
        },
    )

    image1 = image_service.add(
        book.id,
        ImageCreate(url="https://dummyimage.com/780x968"),
    )

    image2 = image_service.add(
        book.id,
        ImageCreate(url="https://dummyimage2.com/800x968"),
    )
    image3 = image_service.add(
        game.id,
        ImageCreate(url="https://dummyimage3.com/800x968"),
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
    product = product_service.add("book", data)

    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))
    # new_data = data.copy()
    new_data = {"url": "https://dummyimage2.com/800x968"}
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
    product = product_service.add("book", data)

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
    product = product_service.add("book", data)
    data = fake_image()
    image = image_service.add(product.id, ImageCreate(**data))

    response = client.delete(f"/products/{product.id}/images/{image.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    image = db.execute(select(Image).where(Image.id == image.id)).scalar_one_or_none()  # type: ignore
    assert image is None


def test_delete_image_not_found(client: TestClient, product_service: ProductService):
    data = fake_product()
    product = product_service.add("book", data)
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
    book = product_service.add(
        "book",
        {
            "name": "Dune",
            "spec_sheet": "Specs...",
            "author": "Frank Herbert",
            "pages": 900,
        },
    )

    image_service.add(
        book.id,
        ImageCreate(url="https://dummyimage.com/780x968"),
    )

    image_service.add(
        book.id,
        ImageCreate(url="https://dummyimage2.com/800x968"),
    )

    image_service.add(
        book.id,
        ImageCreate(url="https://dummyimage3.com/800x968"),
    )

    response = client.delete(f"/products/{book.id}/images")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    cards = db.execute(select(Image).where(Image.id_product == book.id)).all()
    assert len(cards) == 0
