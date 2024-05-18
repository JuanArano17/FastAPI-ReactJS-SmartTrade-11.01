import random
import string
from faker import Faker
from datetime import datetime, timedelta

from app.database import SessionLocal as get_db
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
from app.schemas.orders.order import OrderCreate
from app.service.users.types.user import UserService
from app.schemas.users.types.admin import AdminCreate
from app.service.users.types.admin import AdminService
from app.schemas.products.categories.variations.size import SizeCreate
from app.models.users.in_shopping_cart import InShoppingCart
from app.schemas.users.country import CountryCreate
from app.service.users.country import CountryService
import pycountry

from app.schemas.products.review import ReviewCreate
from app.service.products.review import ReviewService

session = get_db()
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
#    in_shopping_cart_service,
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

review_service = ReviewService(session=session, seller_product_service=seller_product_serv, buyer_service=buyer_service)

admin_service = AdminService(session=session, user_service=user_service)


# Clean up the database before populating it
user_service.delete_all()
product_service.delete_all()
country_service.delete_all()
order_service.delete_all()

# Initialize Faker with a specific seed (for consistency)
faker = Faker()
Faker.seed(42)  # Set the seed to any value you prefer


# Define the number of items to create
# Number of orders must be smaller than number of buyers...
num_buyers = 100
num_sellers = 100
num_cards = 100
num_books = 20
num_games = 20
num_electronics = 20
num_electrodomestics = 20
num_foods = 20
num_clothes = 20
num_house_utilities = 20
num_addresses = 100
num_seller_products = 140
num_cart_items = 100
num_list_items = 100
num_orders = 60
num_product_lines_per_order = 2
num_rejected = 20
num_approved = 100
num_reviews = 100


# # Initialize SQLAlchemy session
# engine = get_engine()
# Session = sessionmaker(bind=engine)
# session = Session()

all_countries = list(pycountry.countries)
for country in all_countries:
    country = CountryCreate(name=country.name)
    country_service.add(country)

admin_service.add(
    AdminCreate(
        email="admin@example.com", name="Robert", surname="House", password="admin"
    )
)

used_emails = []
used_dnis = []


# Create 100 buyers with consistent random data
for i in range(num_buyers):
    # Generate random data for each buyer
    dni_digits = "".join(random.choices(string.digits, k=8))  # Generate 8 random digits
    dni_letter = random.choice(
        string.ascii_uppercase
    )  # Generate a random uppercase letter
    dni = dni_digits + dni_letter  # Concatenate the digits and letter to form the DNI

    buyer_data = {
        "email": faker.email(),
        "name": faker.first_name(),
        "surname": faker.last_name(),
        "birth_date": faker.date_of_birth(minimum_age=15, maximum_age=80),
        "eco_points": 0.0,
        "dni": dni,
        "billing_address": faker.address(),
        "payment_method": "Credit Card",
        "password": "prueba",
    }

    while buyer_data["email"] in used_emails:
        buyer_data["email"] = faker.email()
    while buyer_data["dni"] in used_dnis:
        dni_digits = "".join(
            random.choices(string.digits, k=8)
        )  # Generate 8 random digits
        dni_letter = random.choice(
            string.ascii_uppercase
        )  # Generate a random uppercase letter
        dni = (
            dni_digits + dni_letter
        )  # Concatenate the digits and letter to form the DNI
    used_emails.append(buyer_data["email"])
    used_dnis.append(buyer_data["dni"])
    # Create a BuyerCreate object
    buyer_create = BuyerCreate(**buyer_data)
    # Add the buyer to the database
    buyer_service.add(buyer_create)

used_cifs = []
# Create 100 random sellers
for i in range(num_sellers):
    # Generate random data for each seller
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
        "password": "prueba",
    }

    while seller_data["email"] in used_emails:
        seller_data["email"] = faker.email()
    while seller_data["cif"] in used_cifs:
        cif = "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
            random.choices(string.digits, k=8)
        )
    used_emails.append(seller_data["email"])
    used_cifs.append(seller_data["cif"])

    # Create a SellerCreate object
    seller_create = SellerCreate(**seller_data)

    # Add the seller to the database
    seller_service.add(seller_create)


buyer_ids = buyer_service.buyer_repo.get_id_list()

# Create 100 random cards
for i in range(num_cards):
    # Generate random data for each card
    card_number = faker.credit_card_number(
        card_type=None
    )  # Generate a random card number
    card_name = faker.name()  # Generate a random cardholder name
    card_exp_date = faker.date_between(
        start_date=datetime.now(), end_date="+10y"
    )  # Generate a random expiration date within the next 10 years
    card_security_num = faker.credit_card_security_code(
        card_type=None
    )  # Generate a random security number (CVV)

    # Create a CardCreate object
    card_create = CardCreate(
        card_number=card_number,
        card_name=card_name,
        card_exp_date=card_exp_date,
        card_security_num=card_security_num,
    )

    # Add the card using the CardService
    card_service.add(id_buyer=random.choice(buyer_ids), card=card_create)


# Define length constraints for name and description
name_min_length = 1
name_max_length = 20
description_min_length = 1

for i in range(num_addresses):
    # Generate random data for each address
    street = faker.street_address()
    floor = random.randint(1, 200)
    door = str(faker.building_number())
    adit_info = faker.text(max_nb_chars=69)
    city = faker.city()
    postal_code = faker.postcode()
    country = random.choice(all_countries).name
    default = random.choice([True, False])

    # Create a AddressCreate object
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

    address_service.add(random.choice(buyer_ids), address=address_create)

# Generate and add random products
for _ in range(num_books):
    # Generate random data for each product
    name = faker.catch_phrase()  # Generate a random product name
    name = name[:39]
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    pages = random.randint(100, 1500)
    author = faker.name()
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "pages": pages,
        "author": author,
    }

    # Add the product to the session
    created_product = product_service.add(category="book", product_data=product)

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_games):
    # Generate random data for each product
    name = faker.catch_phrase()  # Generate a random product name
    name = name[:39]
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    publisher = faker.company()
    platform = random.choice(
        [
            "PlayStation",
            "Xbox",
            "Nintendo Switch",
            "PC",
            "Sega Genesis",
            "Atari",
            "GameCube",
            "Wii",
            "Dreamcast",
            "Game Boy",
        ]
    )
    size = str(random.randint(1, 1000)) + "GB"
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "publisher": publisher,
        "platform": platform,
        "size": size,
    }

    # Add the product to the session
    created_product = product_service.add(category="game", product_data=product)

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_clothes):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    materials = random.choice(
        [
            "Cotton",
            "Polyester",
            "Wool",
            "Silk",
            "Denim",
            "Leather",
            "Linen",
            "Velvet",
            "Satin",
            "Nylon",
        ]
    )
    type = random.choice(
        [
            "T-shirt",
            "Jeans",
            "Dress",
            "Skirt",
            "Sweater",
            "Jacket",
            "Shorts",
            "Blouse",
            "Pants",
            "Coat",
        ]
    )
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "materials": materials,
        "type": type,
        # "size": size,
    }

    # Add the product to the session
    created_product = product_service.add(category="clothes", product_data=product)

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_electronics):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    brand = faker.company()
    type = random.choice(
        [
            "Smartphone",
            "Laptop",
            "Tablet",
            "Smartwatch",
            "Headphones",
            "Camera",
            "Television",
            "Speaker",
            "Gaming Console",
            "Router",
        ]
    )
    capacity = str(random.randint(1, 1000)) + "GB"
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "brand": brand,
        "type": type,
        "capacity": capacity,
    }

    # Add the product to the session
    created_product = product_service.add(category="electronics", product_data=product)

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_electrodomestics):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    brand = faker.company()
    type = random.choice(
        [
            "Refrigerator",
            "Washing Machine",
            "Dishwasher",
            "Microwave Oven",
            "Vacuum Cleaner",
            "Coffee Maker",
            "Air Conditioner",
            "Water Heater",
            "Toaster",
            "Blender",
        ]
    )
    power_source = random.choice(["Batteries", "Electrical"])
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "brand": brand,
        "type": type,
        "power_source": power_source,
    }

    # Add the product to the session
    created_product = product_service.add(
        category="electrodomestics", product_data=product
    )

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_house_utilities):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    brand = faker.company()
    type = random.choice(
        [
            "Knife",
            "Fork",
            "Spoon",
            "Plate",
            "Bowl",
            "Cup",
            "Mug",
            "Serving Tray",
            "Cutting Board",
            "Pot",
            "Pan",
            "Whisk",
            "Spatula",
            "Tongs",
            "Grater",
            "Colander",
        ]
    )
    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "brand": brand,
        "type": type,
    }

    # Add the product to the session
    created_product = product_service.add(
        category="houseutilities", product_data=product
    )

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

# Generate and add random products
for _ in range(num_foods):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0
    brand = faker.company()
    type = random.choice(
        [
            "Fruit",
            "Vegetable",
            "Grain",
            "Meat",
            "Fish",
            "Dairy",
            "Bread",
            "Pastry",
            "Snack",
            "Condiment",
            "Beverage",
            "Dessert",
        ]
    )
    ingredients = random.choice(
        ["Protein", "Carbohydrates", "Fats", "Vitamins", "Minerals", "Fiber", "Water"]
    )
    stock = 0

    # Create a Product object
    product = {
        "name": name,
        "description": description,
        "spec_sheet": spec_sheet,
        "stock": stock,
        "brand": brand,
        "type": type,
        "ingredients": ingredients,
    }

    # Add the product to the session
    created_product = product_service.add(category="food", product_data=product)

    num_iterations = random.randint(1, 5)

    for _ in range(num_iterations):
        url = faker.image_url()
        image_create = ImageCreate(url=url)
        image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

product_ids = product_service.product_repo.get_id_list()
seller_ids = seller_service.seller_repo.get_id_list()
used_product_ids = set()


for _ in range(num_seller_products):
    # Choose a unique product ID
    id_product = random.choice(product_ids)
    while id_product in used_product_ids:
        id_product = random.choice(product_ids)
    used_product_ids.add(id_product)

    quantity = random.randint(11, 100)
    price = round(random.uniform(1.0, 100.0), 2)
    remaining_quantity = quantity
    shipping_costs = round(random.uniform(1.0, 20.0), 2)
    product = product_service.get_by_id(id_product)
    sizes = []
    if product.__class__.__name__ == "Clothes":
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
            sizes.append(SizeCreate(size=size, quantity=quantity_per_size).model_dump())
            remaining_quantity -= quantity_per_size

    seller_product = SellerProductCreate(
        quantity=quantity,
        price=price,
        shipping_costs=shipping_costs,
        id_product=id_product,
        sizes=sizes,
    )
    # Add the seller product to the session
    seller_product = seller_product_serv.add(
        id_seller=random.choice(seller_ids), seller_product=seller_product
    )

seller_product_ids = seller_product_serv.seller_product_repo.get_id_list()

for i in range(num_rejected):
    # Create a SellerProduct object
    seller_product = SellerProductUpdate(
        state="Rejected", justification=faker.text(max_nb_chars=49)
    )

    # Add the seller product to the session
    seller_product_serv.update(
        seller_product_id=seller_product_ids[i], new_data=seller_product
    )

for i in range(num_approved):
    # Create a SellerProduct object
    seller_product = SellerProductUpdate(
        state="Approved",
        eco_points=round(
            random.uniform(0, 100), 2
        ),  # Generate a random eco points value
        age_restricted=random.choice([True, False]),
    )

    # Add the seller product to the session
    seller_product_serv.update(
        seller_product_id=seller_product_ids[i + 1 + num_rejected],
        new_data=seller_product,
    )

for _ in range(num_cart_items):
    # Generate random data for each in shopping cart item
    quantity = random.randint(1, 10)  # Random quantity between 1 and 10
    id_seller_product = random.choice(seller_product_ids)

    # Choose a buyer ID
    id_buyer = random.choice(buyer_ids)
    counter = 0
    while in_shopping_cart_service.cart_repo.get_where(
        InShoppingCart.id_buyer == id_buyer,
        InShoppingCart.id_seller_product == id_seller_product,
    ):
        id_buyer = random.choice(buyer_ids)

    # Create an InShoppingCart object
    in_shopping_cart = InShoppingCartCreate(
        id_seller_product=id_seller_product, quantity=quantity
    )
    # Add the in shopping cart item to the session

    seller_product = seller_product_serv.get_by_id(id_seller_product)

    id_size = None
    if seller_product.sizes != []:
        size_ids = []
        for size in seller_product.sizes:
            size_ids.append(size.id)

        id_size = random.choice(size_ids)
        random_size = seller_product_serv.size_repo.get_by_id(id_size)
        while random_size.quantity < quantity:
            id_size = random.choice(size_ids)
            random_size = seller_product_serv.size_repo.get_by_id(id_size)
        in_shopping_cart_service.add(
            id_buyer=id_buyer, shopping_cart_product=in_shopping_cart, id_size=id_size
        )
    else:
        in_shopping_cart_service.add(
            id_buyer=id_buyer, shopping_cart_product=in_shopping_cart
        )


for _ in range(num_list_items):
    # Choose a buyer ID
    id_buyer = random.choice(buyer_ids)
    id_seller_product = random.choice(seller_product_ids)

    while in_wish_list_service.wishlist_repo.get_by_id(
        id_buyer=id_buyer, id_seller_product=id_seller_product
    ):
        id_buyer = random.choice(buyer_ids)

    # Create an wish list object
    in_wish_list = InWishListCreate(id_seller_product=id_seller_product)
    # Add the wish list item to the session
    in_wish_list_service.add(id_buyer=id_buyer, wish_list_item=in_wish_list)

for _ in range(num_reviews):
    # Choose a buyer ID
    id_buyer = random.choice(buyer_ids)
    id_seller_product = random.choice(seller_product_ids)
    while review_service.review_repo.get_repeat_review(id_buyer=id_buyer, id_seller_product=id_seller_product)!=[]:
        id_buyer = random.choice(buyer_ids)
        print(review_service.review_repo.get_repeat_review(id_buyer=id_buyer, id_seller_product=id_seller_product))

    # Create an wish list object
    data={"stars":random.randint(1,5), "comment":faker.text(max_nb_chars=40), "id_seller_product":id_seller_product}
    review = ReviewCreate(**data)
    # Add the wish list item to the session
    review_service.add(id_buyer=id_buyer, review=review)

# Generate and add orders
for i in range(num_orders):
    # Generate random data for each order
    order_date = datetime.now() - timedelta(
        days=random.randint(1, 30)
    )  # Random date within the past 30 days
    buyer = buyer_service.get_by_id(buyer_ids[i])
    cards = buyer.cards
    addresses = buyer.addresses
    while len(cards) < 1 or len(addresses) < 1:
        i += 1
        buyer = buyer_service.get_by_id(buyer_ids[i])
        cards = buyer.cards
        addresses = buyer.addresses

    # Create an Order object
    order = OrderCreate(
        id_card=random.choice(cards).id,
        id_address=random.choice(addresses).id,
        order_date=order_date,
        total=0,
    )

    # Add the order to the session
    created_order = order_service.add(id_buyer=buyer_ids[i], order=order)
    used_seller_product_ids = set()
    for j in range(num_product_lines_per_order):
        # Generate random values for product line attributes
        quantity = random.randint(1, 6)
        # Choose a seller product randomly (ensure it's not a duplicate)
        while True:
            seller_product_id = random.choice(seller_product_ids)
            if seller_product_id not in used_seller_product_ids:
                used_seller_product_ids.add(seller_product_id)
                break
        seller_product = seller_product_serv.get_by_id(seller_product_id)
        price = seller_product.price
        subtotal = quantity * price

        if quantity < seller_product.quantity:
            product_line = ProductLineCreate(
                quantity=quantity,
                subtotal=subtotal,
                id_seller_product=seller_product.id,
            )
            product_line_service.add(
                id_order=created_order.id,
                id_buyer=buyer_ids[i],
                product_line=product_line,
            )

product_line_ids = product_line_service.product_line_repo.get_id_list()

for _ in range(20):
    # Generate random data for each refund product
    id_product_line = random.choice(product_line_ids)
    product_line = product_line_service.product_line_repo.get_by_id(id_product_line)
    quantity = random.randint(1, 3)  # Random quantity between 1 and 3
    order = order_service.get_by_id(product_line.id_order)
    while product_line.quantity < quantity:
        id_product_line = random.choice(product_line_ids)
        product_line = product_line_service.get_by_id(id_product_line)
        order = order_service.get_by_id(product_line.id_order)
    # Generate a random refund date within the past 30 days
    refund_date = product_line.order.order_date + timedelta(days=random.randint(1, 30))

    # Create a RefundProduct object
    refund_product = RefundProductCreate(quantity=quantity, refund_date=refund_date)
    buyer = buyer_service.get_by_id(order.id_buyer)
    # Add the refund product to the session
    refund_product_service.add(
        id_buyer=buyer.id,
        id_order=order.id,
        id_product_line=id_product_line,
        refund_product=refund_product,
    )

# Close the session
session.close()
