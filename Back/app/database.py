from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from local_settings import postgresql as settings
from models.address import Base as AddressBase
from models.order import Base as OrderBase
from models.buyer_owns_card import Base as BuyerOwnsCardBase
from models.product_seller import Base as ProductSellerBase
from models.card import Base as CardBase
from models.product_line import Base as ProductLineBase
from models.refund_product import Base as RefundProductBase
from models.buyer_address import Base as BuyerAddressBase
from models.category import Base as CategoryBase
from models.image import Base as ImageBase
from models.in_shopping_cart import Base as InShoppingCartBase
from models.in_wish_list import Base as InWishListBase
from models.product import Base as ProductBase
from models.seller import Base as SellerBase
from models.buyer import Base as BuyerBase


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_engine_from_settings():
    keys = ["pguser", "pgpasswd", "pghost", "pgport", "pgdb"]
    if not all(key in keys for key in settings.keys()):
        raise Exception("Bad Config File")
    return get_engine(
        settings["pguser"],
        settings["pgpasswd"],
        settings["pghost"],
        settings["pgport"],
        settings["pgdb"],
    )


def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)
    AddressBase.metadata.create_all(bind=engine)
    BuyerOwnsCardBase.metadata.create_all(bind=engine)
    CardBase.metadata.create_all(bind=engine)
    OrderBase.metadata.create_all(bind=engine)
    ProductLineBase.metadata.create_all(bind=engine)
    ProductSellerBase.metadata.create_all(bind=engine)
    RefundProductBase.metadata.create_all(bind=engine)
    ProductBase.metadata.create_all(bind=engine)
    SellerBase.metadata.create_all(bind=engine)
    BuyerBase.metadata.create_all(bind=engine)
    ImageBase.metadata.create_all(bind=engine)
    InShoppingCartBase.metadata.create_all(bind=engine)
    InWishListBase.metadata.create_all(bind=engine)
    CategoryBase.metadata.create_all(bind=engine)
    BuyerAddressBase.metadata.create_all(bind=engine)

    return session
