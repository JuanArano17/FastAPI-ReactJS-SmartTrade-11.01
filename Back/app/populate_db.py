import random
import string
from app.service.seller import SellerService
from app.service.buyer import BuyerService
from app.service.card import CardService
from app.service.category import CategoryService
from app.database import get_db
from datetime import datetime, timedelta
from app.service.seller_product import SellerProductService
from app.schemas.address import AddressCreate
from app.schemas.buyer import BuyerCreate
from app.schemas.card import CardCreate
from app.schemas.category import CategoryCreate
from app.schemas.image import ImageCreate
from app.schemas.in_shopping_cart import InShoppingCartCreate
from app.schemas.in_wish_list import InWishListCreate
from app.schemas.product import ProductCreate
from app.schemas.product_line import ProductLineCreate
from app.schemas.seller import SellerCreate
from app.schemas.seller_product import SellerProductCreate
from app.service.image import ImageService
from app.service.product import ProductService
from app.service.address import AddressService
from app.service.in_shopping_cart import InShoppingCartService
from app.service.in_wish_list import InWishListService
from app.service.order import OrderService
from app.service.product_line import ProductLineService
from app.service.refund_product import RefundProductService
from app.schemas.refund_product import RefundProductCreate
from app.schemas.order import OrderCreate
from app.service.user import UserService
from sqlalchemy.orm import sessionmaker
from app.database import get_engine
from faker import Faker


session = get_db()
user_service = UserService(session=session)
buyer_service = BuyerService(session, user_service=user_service)
seller_service = SellerService(session, user_service=user_service)
category_service = CategoryService(session)
product_service = ProductService(session)
image_service = ImageService(session, product_service)
card_service = CardService(session, buyer_service=buyer_service)
address_service = AddressService(session, buyer_service)
order_service = OrderService(session, buyer_service, card_service, address_service)
seller_product_serv = SellerProductService(
    session, seller_service=seller_service, product_service=product_service
)
in_shopping_cart_service = InShoppingCartService(
    session, buyer_service, seller_product_serv
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


# Initialize Faker with a specific seed (for consistency)
faker = Faker()
Faker.seed(42)  # Set the seed to any value you prefer


# Define the number of items to create
# Number of orders must be smaller than number of buyers...
num_buyers = 100
num_sellers = 100
num_cards = 100
num_categories = 10
num_images = 100
num_products = 100
num_addresses = 100
num_seller_products = 100
num_cart_items = 100
num_list_items = 100
num_orders = 40
num_product_lines_per_order = 2


# Initialize SQLAlchemy session
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

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
        "eco_points": 0.0,
        "dni": dni,
        "billing_address": faker.address(),
        "payment_method": random.choice(["Credit Card", "PayPal", "Bizum"]),
        "password": faker.password(length=12),
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
        "cif": cif,
        "bank_data": bank_data,
        "password": faker.password(length=12),
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


# Create 10 random categories
for i in range(num_categories):
    # Generate random data for each category
    category_name = faker.word()[:name_max_length]  # Truncate to ensure max length
    category_description = faker.text(max_nb_chars=69)  # Limit to max length

    # Create a CategoryCreate object
    category_create = CategoryCreate(
        name=category_name, description=category_description
    )

    # Add the category to the database
    category_service.add(category_create)

category_ids = category_service.category_repo.get_id_list()

for i in range(num_addresses):
    # Generate random data for each address
    street = faker.street_address()
    floor = random.randint(1, 200)
    door = str(faker.building_number())
    adit_info = faker.text(max_nb_chars=69)
    city = faker.city()
    postal_code = faker.postcode()
    country = faker.country_code(representation="alpha-3")
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
for _ in range(num_products):
    # Generate random data for each product
    name = faker.word()  # Generate a random product name
    description = faker.sentence()  # Generate a random product description
    eco_points = round(random.uniform(0, 100), 2)  # Generate a random eco points value
    spec_sheet = faker.text(max_nb_chars=200)  # Generate a random specification sheet
    stock = 0

    # Create a Product object
    product = ProductCreate(
        name=name,
        description=description,
        eco_points=eco_points,
        spec_sheet=spec_sheet,
        stock=stock,
    )

    # Add the product to the session
    created_product = product_service.add(
        id_category=random.choice(category_ids), product=product
    )

    url = faker.image_url()
    image_create = ImageCreate(url=url)
    image_service.add(id_product=created_product.id, image=image_create)

    # Assuming session is your SQLAlchemy session object

product_ids = product_service.product_repo.get_id_list()
seller_ids = seller_service.seller_repo.get_id_list()
used_product_ids = set()

for _ in range(num_seller_products):
    # Generate random data for each seller product
    quantity = random.randint(11, 100)
    price = round(random.uniform(1.0, 100.0), 2)
    shipping_costs = round(random.uniform(1.0, 20.0), 2)

    # Choose a unique product ID
    id_product = random.choice(product_ids)
    while id_product in used_product_ids:
        id_product = random.choice(product_ids)
    used_product_ids.add(id_product)

    # Create a SellerProduct object
    seller_product = SellerProductCreate(
        quantity=quantity,
        price=price,
        shipping_costs=shipping_costs,
        id_product=id_product,
    )

    # Add the seller product to the session
    seller_product_serv.add(
        id_seller=random.choice(seller_ids), seller_product=seller_product
    )

seller_product_ids = seller_product_serv.seller_product_repo.get_id_list()

for _ in range(num_cart_items):
    # Generate random data for each in shopping cart item
    quantity = random.randint(1, 10)  # Random quantity between 1 and 10
    id_seller_product = random.choice(seller_product_ids)

    # Choose a buyer ID
    id_buyer = random.choice(buyer_ids)
    while in_shopping_cart_service.cart_repo.get_by_id(
        id_buyer=id_buyer, id_seller_product=id_seller_product
    ):
        id_buyer = random.choice(buyer_ids)

    # Create an InShoppingCart object
    in_shopping_cart = InShoppingCartCreate(
        id_seller_product=id_seller_product, quantity=quantity
    )
    # Add the in shopping cart item to the session

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
