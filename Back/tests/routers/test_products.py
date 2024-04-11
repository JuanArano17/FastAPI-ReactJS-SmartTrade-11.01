from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.buyer import BuyerCreate
from app.models.product import Product
from app.models.food import Food
from app.service.buyer import BuyerService
from app.service.product import ProductService


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

def fake_game():
    return {
        "name": "gta6",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 10,
        "publisher": "Rockstar",
        "platform": "ps5",
        "size":"100GB",
    }

def fake_electronics():
    return {
        "name": "EliteBook",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 9,
        "brand": "HP",
        "type": "PC",
        "capacity": "1000GB",
    }

def fake_electrodomestics():
    return {
        "name": "toaster",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 19,
        "brand": "Bosch",
        "type": "kitchen electro",
        "power_source": "batteries",
    }

def fake_food():
    return {
        "name": "toaster",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 19,
        "brand": "Kellogs",
        "type": "cereal",
        "ingredients": "carbs 500g, protein 300g",
    }

def fake_house_utilities():
    return {
        "name": "three pointed forks",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 19,
        "brand": "fork s.a",
        "type": "forks",
    }

def fake_clothes():
    return {
        "name": "Nike shirt",
        "description":None,
        "spec_sheet": "Specs...",
        "stock":0,
        "eco_points": 19,
        "materials": "cotton, wool",
        "type": "T-shirt",
        "size": "M",
    }


def test_create_book(client: TestClient, product_service: ProductService, db: Session):
    data = fake_book()

    response = client.post("/products/?category_name=book", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["author"] == data["author"]
    assert content["pages"] == data["pages"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None


def test_create_game(client: TestClient, product_service: ProductService, db: Session):
    data = fake_game()

    response = client.post("/products/?category_name=game", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["publisher"] == data["publisher"]
    assert content["platform"] == data["platform"]
    assert content["size"] == data["size"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None


def test_create_electronics(client: TestClient, product_service: ProductService, db: Session):
    data = fake_electronics()

    response = client.post("/products/?category_name=electronics", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert "capacity" in content
    assert content["capacity"] == data["capacity"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None

def test_create_electrodomestics(client: TestClient, product_service: ProductService, db: Session):
    data = fake_electrodomestics()

    response = client.post("/products/?category_name=electrodomestics", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert content["power_source"] == data["power_source"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None

def test_create_food(client: TestClient, product_service: ProductService, db: Session):
    data = fake_food()

    response = client.post("/products/?category_name=food", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert content["ingredients"] == data["ingredients"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None


def test_create_house_utilities(client: TestClient, product_service: ProductService, db: Session):
    data = fake_house_utilities()

    response = client.post("/products/?category_name=houseutilities", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None


def test_create_clothes(client: TestClient, product_service: ProductService, db: Session):
    data = fake_clothes()

    response = client.post("/products/?category_name=clothes", json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["size"] == data["size"]
    assert content["materials"] == data["materials"]
    assert "id" in content

    product = product_service.get_by_id(content["id"])
    assert product is not None


def test_create_product_invalid_data(client: TestClient):
    data = fake_clothes()
    data["size"] = "N"  # Invalid clothes size

    response = client.post("/products/?category_name=clothes", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_product_invalid_category(client: TestClient):
    data = fake_game()

    response = client.post("/products/?category_name=ga", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_create_product_wrong_category(client: TestClient):
    data = fake_book()

    response = client.post("/products/?category_name=electronics", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_get_book_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_book()
    product = product_service.add("book", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["author"] == data["author"]
    assert content["pages"] == data["pages"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_game_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_game()
    product = product_service.add("game", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["publisher"] == data["publisher"]
    assert content["platform"] == data["platform"]
    assert content["size"] == data["size"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_electronics_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_electronics()
    product = product_service.add("electronics", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert content["capacity"] == data["capacity"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_electrodomestics_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_electrodomestics()
    product = product_service.add("electrodomestics", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert content["power_source"] == data["power_source"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_house_utilities_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_house_utilities()
    product = product_service.add("houseutilities", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_food_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_food()
    product = product_service.add("food", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["brand"] == data["brand"]
    assert content["ingredients"] == data["ingredients"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_clothes_by_id(client: TestClient, product_service: ProductService, db: Session):
    data = fake_clothes()
    product = product_service.add("clothes", data)

    response = client.get(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == data["name"]
    assert content["spec_sheet"] == data["spec_sheet"]
    assert content["stock"] == data["stock"]
    assert content["description"] == data ["description"]
    assert content["eco_points"] == data["eco_points"]
    assert content["type"] == data["type"]
    assert content["size"] == data["size"]
    assert content["materials"] == data["materials"]
    assert "id" in content
    assert content["id"] == product.id  # type: ignore


def test_get_product_not_found(
    client: TestClient, product_service: ProductService, db: Session
):
    response = client.get("/products/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Product with id 999 not found."


def test_get_products(client: TestClient, product_service: ProductService, db: Session):
    book = product_service.add("book", fake_book())
    game = product_service.add("game", fake_game())
    electronics = product_service.add("electronics", fake_electronics())
    electrodomestics = product_service.add("electrodomestics", fake_electrodomestics())
    food = product_service.add("food", fake_food())
    house_utilities = product_service.add("houseutilities", fake_house_utilities())
    clothes = product_service.add("clothes", fake_clothes())

    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    #assert len(content) == 7
    assert book.id in [product["id"] for product in content]
    assert game.id in [product["id"] for product in content]
    assert electronics.id in [product["id"] for product in content]
    assert electrodomestics.id in [product["id"] for product in content]
    assert house_utilities.id in [product["id"] for product in content]
    assert food.id in [product["id"] for product in content]
    assert clothes.id in [product["id"] for product in content]

    assert book.name in [product["name"] for product in content]
    assert game.publisher in [product["publisher"] for product in content]


def test_update_product(client: TestClient, product_service: ProductService, db: Session):
    data = fake_electronics()
    product = product_service.add("electronics", data)

    new_data = {
        "name": "Laptop",
    }

    response = client.put(f"/products/{product.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["name"] == new_data["name"]
    assert "id" in content

    new_data = {
        "type": "Laptop",
    }
    response = client.put(f"/products/{product.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["type"] == new_data["type"]
    assert "id" in content

    new_data = {
        "description": "cool laptop",
        "capacity" : "900GB",
    }
    response = client.put(f"/products/{product.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["description"] == new_data["description"]
    assert content["capacity"] == new_data["capacity"]
    assert "id" in content

def test_update_product_invalid_data(
    client: TestClient, product_service: ProductService, db: Session
):
    data = fake_book()
    product = product_service.add("book", data)

    new_data = data.copy()
    new_data["name"] = "New Name"
    new_data["description"] = "New Desc"
    new_data["spec_sheet"] = "123"  
    new_data["eco_points"] = 100
    new_data["author"] = "Me"
    new_data["pages"] = "x" #invalid page number

    response = client.put(f"/products/{product.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

    new_data={"publisher": "me"} #wrong keyword
    response = client.put(f"/products/{product.id}", json=new_data)  # type: ignore
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()



def test_delete_product(client: TestClient, product_service: ProductService, db: Session):
    data = fake_food()
    product = product_service.add("food",data)

    response = client.delete(f"/products/{product.id}")  # type: ignore
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    product1 = db.execute(select(Product).where(Product.id == product.id)).scalar_one_or_none()  # type: ignore
    assert product1 is None
    product1 = db.execute(select(Food).where(Food.id == product.id)).scalar_one_or_none()  # type: ignore
    assert product1 is None

def test_delete_product_not_found(client: TestClient):
    response = client.delete("/products/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == "Product with id 999 not found."


def test_delete_products(client: TestClient, product_service: ProductService, db: Session):
    game = product_service.add("game", fake_game())
    electronics = product_service.add("electronics", fake_electronics())
    electrodomestics=product_service.add("electrodomestics", fake_electrodomestics())
    food=product_service.add("food", fake_food())
    house_utilities=product_service.add("houseutilities", fake_house_utilities())
    clothes=product_service.add("clothes", fake_clothes())

    response = client.delete("/products/")
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content is None or content == {}

    products = db.execute(select(Product)).all()
    assert len(products) == 0