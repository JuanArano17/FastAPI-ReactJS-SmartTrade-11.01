import random
import requests
import pycountry
import string
from faker import Faker
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import your services and models here
from app.database import SessionLocal
from app.core.enums import OrderState
from app.service.users.types.seller import SellerService
from app.service.users.types.buyer import BuyerService
from app.service.users.card import CardService
from app.service.products.seller_product import SellerProductService
from app.schemas.users.address import AddressCreate
from app.schemas.users.types.buyer import BuyerCreate
from app.schemas.users.card import CardCreate
from app.schemas.products.image import ImageCreate
from app.schemas.users.in_shopping_cart import InShoppingCartCreate
from app.schemas.users.in_wish_list import InWishListCreate
from app.schemas.orders.order import ConfirmOrder
from app.schemas.orders.product_line import ProductLineCreate
from app.schemas.users.types.seller import SellerCreate
from app.schemas.products.seller_product import SellerProductCreate, SellerProductUpdate
from app.service.products.image import ImageService
from app.service.products.product import ProductService
from app.service.users.address import AddressService
from app.service.users.in_shopping_cart import InShoppingCartService
from app.service.users.in_wish_list import InWishListService
from app.service.orders.order import OrderService
from app.service.orders.product_line import ProductLineService
from app.service.orders.refund_product import RefundProductService
from app.schemas.orders.refund_product import RefundProductCreate
from app.service.users.types.user import UserService
from app.schemas.users.types.admin import AdminCreate
from app.service.users.types.admin import AdminService
from app.schemas.products.categories.variations.size import SizeCreate
from app.models.users.in_shopping_cart import InShoppingCart
from app.schemas.users.country import CountryCreate
from app.service.users.country import CountryService

from app.schemas.products.review import ReviewCreate
from app.service.products.review import ReviewService

# Initialize Faker with a specific seed (for consistency)
faker = Faker()
Faker.seed(42)  # Set the seed to any value you prefer

# Define the number of items to create
num_buyers = 100
num_sellers = 100
num_cards_per_person=3
num_books = 40
num_games = 40
num_electronics = 40
num_electrodomestics = 40
num_foods = 40
num_clothes = 40
num_house_utilities = 40
num_addresses_per_person = 3
num_seller_products = 280
num_cart_items = 750
num_list_items = 100
num_orders = 63
num_product_lines_per_order = 3
num_rejected = 40
num_approved = 200
num_reviews = 100


def create_services():
    session = SessionLocal()
    user_service = UserService(session=session)
    buyer_service = BuyerService(session, user_service=user_service)
    seller_service = SellerService(session, user_service=user_service)
    product_service = ProductService(session)
    image_service = ImageService(session, product_service)
    card_service = CardService(session, buyer_service=buyer_service)
    address_service = AddressService(session, buyer_service)
    seller_product_serv = SellerProductService(
        session, seller_service=seller_service, product_service=product_service
    )
    in_shopping_cart_service = InShoppingCartService(
        session, buyer_service, seller_product_serv
    )
    order_service = OrderService(
        session,
        buyer_service,
        card_service,
        address_service,
        product_service,
        seller_product_serv,
        in_shopping_cart_service,
    )
    in_wish_list_service = InWishListService(
        session=session,
        buyer_service=buyer_service,
        seller_product_service=seller_product_serv,
    )
    product_line_service = ProductLineService(
        session,
        buyer_service=buyer_service,
        order_service=order_service,
        seller_product_service=seller_product_serv,
    )
    refund_product_service = RefundProductService(
        session=session,
        buyer_service=buyer_service,
        order_service=order_service,
        seller_product_service=seller_product_serv,
        product_line_service=product_line_service,
    )
    country_service = CountryService(session=session)
    review_service = ReviewService(
        session=session,
        seller_product_service=seller_product_serv,
        buyer_service=buyer_service,
    )
    admin_service = AdminService(session=session, user_service=user_service)

    return {
        "session": session,
        "user_service": user_service,
        "buyer_service": buyer_service,
        "seller_service": seller_service,
        "product_service": product_service,
        "image_service": image_service,
        "card_service": card_service,
        "address_service": address_service,
        "seller_product_serv": seller_product_serv,
        "in_shopping_cart_service": in_shopping_cart_service,
        "order_service": order_service,
        "in_wish_list_service": in_wish_list_service,
        "product_line_service": product_line_service,
        "refund_product_service": refund_product_service,
        "country_service": country_service,
        "review_service": review_service,
        "admin_service": admin_service,
    }


def run_in_parallel(tasks, *args):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(task, *args) for task in tasks]
        results = [future.result() for future in as_completed(futures)]
    return results


def initialize_db():
    services = create_services()
    session = services["session"]
    user_service = services["user_service"]
    product_service = services["product_service"]
    country_service = services["country_service"]
    order_service = services["order_service"]

    # Clean up the database before populating it
    user_service.delete_all()
    product_service.delete_all()
    country_service.delete_all()
    order_service.delete_all()

    all_countries = list(pycountry.countries)
    for country in all_countries:
        country = CountryCreate(name=country.name)
        country_service.add(country)

    services["admin_service"].add(
        AdminCreate(
            email="admin@example.com", name="Robert", surname="House", password="admin1234@"
        )
    )
    session.commit()
    session.close()


def create_buyer():
    services = create_services()
    session = services["session"]
    buyer_service = services["buyer_service"]

    dni_digits = "".join(random.choices(string.digits, k=8))
    dni_letter = random.choice(string.ascii_uppercase)
    dni = dni_digits + dni_letter
    buyer_data = {
        "email": faker.email(),
        "name": faker.first_name(),
        "surname": faker.last_name(),
        "birth_date": faker.date_of_birth(minimum_age=15, maximum_age=80),
        "eco_points": 0.0,
        "dni": dni,
        "billing_address": faker.address(),
        "payment_method": "Credit Card",
        "password": "prueba1234@",
    }
    buyer_create = BuyerCreate(**buyer_data)
    buyer = buyer_service.add(buyer_create)
    session.commit()
    buyer_id = buyer.id  # Get the ID before closing the session
    session.close()
    return buyer_id


def create_seller():
    services = create_services()
    session = services["session"]
    seller_service = services["seller_service"]

    cif = "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
        random.choices(string.digits, k=8)
    )
    bank_data = faker.iban()
    seller_data = {
        "email": faker.email(),
        "name": faker.first_name(),
        "surname": faker.last_name(),
        "birth_date": faker.date_of_birth(minimum_age=18, maximum_age=80),
        "cif": cif,
        "bank_data": bank_data,
        "password": "prueba1234@",
    }
    seller_create = SellerCreate(**seller_data)
    seller = seller_service.add(seller_create)
    session.commit()
    seller_id = seller.id  # Get the ID before closing the session
    session.close()
    return seller_id


def create_card_sequential(buyer_ids,i):
    services = create_services()
    session = services["session"]
    card_service = services["card_service"]

    for _ in range(num_cards_per_person):
        card_number = faker.credit_card_number(card_type=None)
        card_name = faker.name()
        card_exp_date = faker.date_between(start_date=datetime.now(), end_date="+10y")
        card_security_num = faker.credit_card_security_code(card_type=None)
        card_create = CardCreate(
            card_number=card_number,
            card_name=card_name,
            card_exp_date=card_exp_date,
            card_security_num=card_security_num,
        )
        card_service.add(id_buyer=buyer_ids[i], card=card_create)
    session.commit()
    session.close()


def create_address_sequential(buyer_ids,i):
    services = create_services()
    session = services["session"]
    address_service = services["address_service"]

    for _ in range(num_addresses_per_person):
        street = faker.street_address()
        floor = random.randint(1, 200)
        door = str(faker.building_number())
        adit_info = faker.text(max_nb_chars=69)
        city = faker.city()
        postal_code = faker.postcode()
        country = faker.country()
        default = random.choice([True, False])
        address_create = AddressCreate(
            street=street,
            floor=floor,
            door=door,
            adit_info=adit_info,
            city=city,
            postal_code=postal_code,
            country=country,
            default=default,
        )
        address_service.add(buyer_ids[i], address=address_create)
    session.commit()
    session.close()


def create_product(category, extra_fields):
    services = create_services()
    session = services["session"]
    product_service = services["product_service"]
    image_service = services["image_service"]

    name = faker.word()[:39]
    description = faker.sentence()
    spec_sheet = faker.text(max_nb_chars=200)
    stock = 0
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
    }
    product.update(extra_fields)
    created_product = product_service.add(category=category, product_data=product)
    used_urls = []
    for _ in range(random.randint(1, 5)):
        # Generar un número aleatorio para evitar caché y obtener una imagen diferente cada vez
        random_param = random.randint(1, 100000)
        if category=="Game":
                url = f"https://source.unsplash.com/featured/?videogame&{random_param}"
        elif category.lower() =="houseutilities":
                url = f"https://source.unsplash.com/featured/?kitchen&{random_param}"
        else:
                url = f"https://source.unsplash.com/featured/?{category}&{random_param}"
        while url in used_urls:
            if category=="Game":
                url = f"https://source.unsplash.com/featured/?videogame&{random_param}"
            elif category.lower() =="houseutilities":
                url = f"https://source.unsplash.com/featured/?kitchen&{random_param}"
            else:
                url = f"https://source.unsplash.com/featured/?{category}&{random_param}"
        used_urls.append(url)
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)
    session.commit()
    created_product_id = created_product.id
    session.close()
    return created_product_id

orders_ids=[]
buyers_with_orders=[]
def create_order_sequential(buyer_ids):
    services = create_services()
    session = services["session"]
    buyer_service = services["buyer_service"]
    order_service = services["order_service"]
    shopping_cart_service = services["in_shopping_cart_service"]
    seller_product_service = services["seller_product_serv"]
    order_date = datetime.now() - timedelta(days=random.randint(1, 30))
    buyer_id = random.choice(buyer_ids)
    buyer = buyer_service.get_by_id(buyer_id)
    cards = buyer.cards
    addresses = buyer.addresses
    print(cards)
    print(addresses)
    order = ConfirmOrder(
        id_card=random.choice(cards).id,
        id_address=random.choice(addresses).id,
    )
    #shopping_cart=shopping_cart_service.get_by_id_buyer(buyer_id)
    #for cart_item in shopping_cart:
    #    seller_product=seller_product_service.get_by_id(cart_item.id_seller_product)
    #    if seller_product.sizes==[]:
    #        if cart_item.quantity>seller_product.quantity:
    #            shopping_cart_service.delete_by_id(cart_item.id)
    #    else:
    #        size=seller_product_service.size_repo.get_by_id(cart_item.id_size)
    #        if cart_item.quantity>seller_product.quantity:
    #            shopping_cart_service.delete_by_id(cart_item.id)
    if(shopping_cart_service.get_by_user(buyer)!=[]):
        created_order = order_service.create_from_shopping_cart(buyer, order)
        order_id = created_order.id  # Obtener el ID antes de cerrar la sesión
        buyer_id = buyer.id  # Obtener el ID antes de cerrar la sesión
        orders_ids.append(order_id)
        session.commit()
        session.close()
        return order_id, buyer_id
    else:
        session.close()

def confirm_order_sequential(i,order_ids):
    services = create_services()
    session = services["session"]
    buyer_service = services["buyer_service"]
    order_service = services["order_service"]
    seller_product_service=services["seller_product_serv"]
    product_line_service=services["product_line_service"]
    order=order_service.order_repo.get_by_id(order_ids[i])
    if order==None:
        return
    
    for product_line in order.product_lines:
        seller_product=seller_product_service.get_by_id(product_line.id_seller_product)
        if seller_product.sizes==[]:
            if product_line.quantity>seller_product.quantity:
                product_line_service.delete_by_id(product_line.id)
        else:
            size=seller_product_service.size_repo.get_by_id(product_line.id_size)
            if product_line.quantity>size.quantity:
                product_line_service.delete_by_id(product_line.id)
            
    buyer_id = order.id_buyer
    buyer = buyer_service.get_by_id(buyer_id)
    cards = buyer.cards
    addresses = buyer.addresses
    if len(cards) < 1 or len(addresses) < 1:
        return
    order = ConfirmOrder(
        id_card=random.choice(cards).id,
        id_address=random.choice(addresses).id,
    )
    created_order = order_service.confirm_pending_order(buyer,order)
    order_id = created_order.id  # Obtener el ID antes de cerrar la sesión
    buyer_id = buyer.id  # Obtener el ID antes de cerrar la sesión
    session.commit()
    session.close()
    return order_id, buyer_id


def create_reviews_sequential(buyer_purchased_products):
    services = create_services()
    session = services["session"]
    review_service = services["review_service"]

    review_count = 0
    reviewed_pairs = set()

    while review_count < num_reviews:
        buyer_id = random.choice(list(buyer_purchased_products.keys()))
        purchased_products = list(buyer_purchased_products[buyer_id])
        if purchased_products:
            id_seller_product = random.choice(purchased_products)
            review_pair = (buyer_id, id_seller_product)
            if review_pair not in reviewed_pairs:
                data = {
                    "stars": random.randint(1, 5),
                    "comment": faker.text(max_nb_chars=40),
                    "id_seller_product": id_seller_product,
                }
                review = ReviewCreate(**data)
                review_service.add(id_buyer=buyer_id, review=review)
                reviewed_pairs.add(review_pair)
                review_count += 1

    session.commit()
    session.close()


def create_refund_products_sequential(product_line_ids):
    services = create_services()
    session = services["session"]
    product_line_service = services["product_line_service"]
    order_service = services["order_service"]
    refund_product_service = services["refund_product_service"]
    buyer_service = services["buyer_service"]

    for _ in range(20):
        id_product_line = random.choice(product_line_ids)
        product_line = product_line_service.product_line_repo.get_by_id(id_product_line)
        quantity = random.randint(1, 3)
        order = order_service.get_by_id(product_line.id_order)
        while product_line.quantity < quantity:
            id_product_line = random.choice(product_line_ids)
            product_line = product_line_service.get_by_id(id_product_line)
            order = order_service.get_by_id(product_line.id_order)
        refund_date = product_line.order.order_date + timedelta(
            days=random.randint(1, 30)
        )
        refund_product = RefundProductCreate(quantity=quantity, refund_date=refund_date)
        buyer = buyer_service.get_by_id(order.id_buyer)
        refund_product_service.add(
            id_buyer=buyer.id,
            id_order=order.id,
            id_product_line=id_product_line,
            refund_product=refund_product,
        )
    session.commit()
    session.close()


# Initialize the database
initialize_db()

# Populate buyers, sellers, and products in parallel
buyer_ids = run_in_parallel([create_buyer] * num_buyers)
seller_ids = run_in_parallel([create_seller] * num_sellers)

for i in range(len(buyer_ids)):
    create_card_sequential(buyer_ids, i)

for i in range(len(buyer_ids)):
    create_address_sequential(buyer_ids, i)


# Populate products in parallel
product_categories = [
    ("book", {"pages": random.randint(100, 1500), "author": faker.name()}),
    (
        "game",
        {
            "publisher": faker.company(),
            "platform": random.choice(["PlayStation", "Xbox", "Nintendo Switch", "PC"]),
            "size": str(random.randint(1, 1000)) + "GB",
        },
    ),
    (
        "clothes",
        {
            "materials": random.choice(["Cotton", "Polyester", "Wool"]),
            "type": random.choice(["T-shirt", "Jeans", "Dress"]),
        },
    ),
    (
        "electronics",
        {
            "brand": faker.company(),
            "type": random.choice(["Smartphone", "Laptop"]),
            "capacity": str(random.randint(1, 1000)) + "GB",
        },
    ),
    (
        "electrodomestics",
        {
            "brand": faker.company(),
            "type": random.choice(["Refrigerator", "Washing Machine"]),
            "power_source": random.choice(["Batteries", "Electrical"]),
        },
    ),
    (
        "houseutilities",
        {"brand": faker.company(), "type": random.choice(["Knife", "Fork"])},
    ),
    (
        "food",
        {
            "brand": faker.company(),
            "type": random.choice(["Fruit", "Vegetable"]),
            "ingredients": random.choice(["Protein", "Carbohydrates"]),
        },
    ),
]

product_ids = []
for category, extra_fields in product_categories:
    product_ids.extend(
        run_in_parallel([lambda: create_product(category, extra_fields)] * num_books)
    )


def create_seller_product_sequential():
    services = create_services()
    session = services["session"]
    product_service = services["product_service"]
    seller_product_serv = services["seller_product_serv"]

    used_product_ids = []
    for i in range(num_seller_products):
        id_product = random.choice(product_ids)
        id_seller = random.choice(seller_ids)

        while id_product in used_product_ids:
            id_product = random.choice(product_ids)

        used_product_ids.append(id_product)

        quantity = random.randint(11, 100)
        price = round(random.uniform(1.0, 100.0), 2)
        remaining_quantity = quantity
        shipping_costs = round(random.uniform(1.0, 20.0), 2)
        product = product_service.get_by_id(id_product)
        sizes = []
        if product.__class__.__name__ == "Clothes":
            print(i)
            i = 0
            used_choices = []
            options = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL"]
            while remaining_quantity > 0:
                size = random.choice(options)
                while size in used_choices:
                    size = random.choice(options)
                used_choices.append(size)
                quantity_per_size = random.randint(1, remaining_quantity)
                if len(used_choices) == len(options):
                    quantity_per_size = remaining_quantity
                sizes.append(
                    SizeCreate(size=size, quantity=quantity_per_size).model_dump()
                )
                remaining_quantity -= quantity_per_size

        seller_product = SellerProductCreate(
            quantity=quantity,
            price=price,
            shipping_costs=shipping_costs,
            id_product=id_product,
            sizes=sizes,
        )
        seller_product_serv.add(id_seller=id_seller, seller_product=seller_product)
    session.commit()
    session.close()


# Ejecutar la creación secuencial de productos de vendedor
create_seller_product_sequential()

services = create_services()
seller_product_ids = services["seller_product_serv"].seller_product_repo.get_id_list()

for i in range(num_rejected):
    services = create_services()
    session = services["session"]
    seller_product_serv = services["seller_product_serv"]

    seller_product = SellerProductUpdate(
        state="Rejected", justification=faker.text(max_nb_chars=49)
    )
    seller_product_serv.update(
        seller_product_id=seller_product_ids[i], new_data=seller_product
    )
    session.commit()
    session.close()

list_of_approved_ids = []

for i in range(num_approved):
    services = create_services()
    session = services["session"]
    seller_product_serv = services["seller_product_serv"]

    seller_product = SellerProductUpdate(
        state="Approved",
        eco_points=round(random.uniform(0, 100), 2),
        age_restricted=random.choice([True, False]),
    )
    seller_product_serv.update(
        seller_product_id=seller_product_ids[i + 1 + num_rejected],
        new_data=seller_product,
    )
    session.commit()
    session.close()
    list_of_approved_ids.append(seller_product_ids[i + 1 + num_rejected])


def create_cart_item_sequential():
    services = create_services()
    session = services["session"]
    in_shopping_cart_service = services["in_shopping_cart_service"]
    seller_product_serv = services["seller_product_serv"]

    quantity = random.randint(1, 10)
    id_seller_product = random.choice(list_of_approved_ids)
    id_buyer = random.choice(buyer_ids)
    while in_shopping_cart_service.cart_repo.get_where(
        InShoppingCart.id_buyer == id_buyer,
        InShoppingCart.id_seller_product == id_seller_product,
    ):
        id_buyer = random.choice(buyer_ids)
    in_shopping_cart = InShoppingCartCreate(
        id_seller_product=id_seller_product, quantity=quantity
    )
    seller_product = seller_product_serv.get_by_id(id_seller_product)
    id_size = None
    if seller_product.sizes:
        quantity = random.randint(1, 4)
        in_shopping_cart = InShoppingCartCreate(
        id_seller_product=id_seller_product, quantity=quantity
        )
        size_ids = [size.id for size in seller_product.sizes]
        id_size = random.choice(size_ids)
        random_size = seller_product_serv.size_repo.get_by_id(id_size)
        while random_size.quantity < quantity:
            id_size = random.choice(size_ids)
            print("h")
            random_size = seller_product_serv.size_repo.get_by_id(id_size)
        in_shopping_cart_service.add(
            id_buyer=id_buyer, shopping_cart_product=in_shopping_cart, id_size=id_size
        )
    else:
        in_shopping_cart_service.add(
            id_buyer=id_buyer, shopping_cart_product=in_shopping_cart
        )
    session.commit()
    session.close()


def create_wish_list_item_sequential():
    services = create_services()
    session = services["session"]
    in_wish_list_service = services["in_wish_list_service"]

    id_buyer = random.choice(buyer_ids)
    id_seller_product = random.choice(list_of_approved_ids)
    while in_wish_list_service.wishlist_repo.get_by_id(
        id_buyer=id_buyer, id_seller_product=id_seller_product
    ):
        id_buyer = random.choice(buyer_ids)
    in_wish_list = InWishListCreate(id_seller_product=id_seller_product)
    in_wish_list_service.add(id_buyer=id_buyer, wish_list_item=in_wish_list)
    session.commit()
    session.close()


# Populate shopping cart and wish list items in parallel
for i in range(num_cart_items):
    create_cart_item_sequential()
for i in range(num_list_items):
    create_wish_list_item_sequential()

#created_orders = run_in_parallel([create_order] * num_orders, buyer_ids)
created_orders=[]
for i in range(num_orders):
    result = create_order_sequential(buyer_ids)
    if result is not None:
        created_orders.append(result)

#confirmed_orders=[]
#for i in range(int(len(orders_ids)*0.95)):
#    confirmed_orders.append(confirm_order_sequential(i,orders_ids))
# Populate product lines for each order en secuencial
#create_product_lines_sequential(created_orders, seller_product_ids)



services = create_services()
product_line_ids = services["product_line_service"].product_line_repo.get_id_list()

buyer_purchased_products = {buyer_id: set() for buyer_id in buyer_ids}
for created_order in created_orders:
    order_id, buyer_id = created_order
    services = create_services()
    session = services["session"]
    product_line_service = services["product_line_service"]

    product_lines = product_line_service.get_all_by_order_id(order_id)
    for product_line in product_lines:
        buyer_purchased_products[buyer_id].add(product_line.id_seller_product)
    session.close()
  
# Crear reviews de manera secuencial
create_reviews_sequential(buyer_purchased_products)

# Crear productos de devolución de manera secuencial
create_refund_products_sequential(product_line_ids)

# Close the session
services = create_services()
session = services["session"]
session.close()
