from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session, selectin_polymorphic
from pydantic import ValidationError

from app.models.admin import Admin
from app.models.buyer import Buyer
from app.models.seller import Seller
from app.models.user import User
from app.database import get_db
from app.schemas.token import TokenPayload
from app.core.security import SECRET_KEY, ALGORITHM

from app.service.user import UserService
from app.service.buyer import BuyerService
from app.service.seller import SellerService
from app.service.address import AddressService
from app.service.card import CardService
from app.service.product import ProductService
from app.service.order import OrderService
from app.service.category import CategoryService
from app.service.product_line import ProductLineService
from app.service.seller_product import SellerProductService
from app.service.refund_product import RefundProductService
from app.service.image import ImageService
from app.service.in_shopping_cart import InShoppingCartService
from app.service.in_wish_list import InWishListService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    loader_opt = selectin_polymorphic(User, [Buyer, Seller, Admin])
    user = session.execute(
        select(User).where(User.email == token_data.sub).options(loader_opt)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUserDep):
    if current_user.type == "Admin":  # type: ignore
        return current_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user does not have enough permissions",
    )


# Services dependencies
def get_user_service(session: SessionDep):
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_buyer_service(session: SessionDep, user_service: UserServiceDep):
    return BuyerService(session=session, user_service=user_service)


BuyerServiceDep = Annotated[BuyerService, Depends(get_buyer_service)]


def get_seller_service(session: SessionDep, user_service: UserServiceDep):
    return SellerService(session=session, user_service=user_service)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]


def get_address_service(session: SessionDep, buyer_service: BuyerServiceDep):
    return AddressService(session=session, buyer_service=buyer_service)


AddressServiceDep = Annotated[AddressService, Depends(get_address_service)]


def get_category_service(session: SessionDep):
    return CategoryService(session=session)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]


def get_card_service(session: SessionDep, buyer_service: BuyerServiceDep):
    return CardService(session=session, buyer_service=buyer_service)


CardServiceDep = Annotated[CardService, Depends(get_card_service)]


def get_product_service(session: SessionDep):
    return ProductService(session=session)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


def get_image_service(session: SessionDep, product_service: ProductServiceDep):
    return ImageService(session=session, product_service=product_service)


ImageServiceDep = Annotated[ImageService, Depends(get_image_service)]


def get_order_service(
    session: SessionDep,
    buyer_service: BuyerServiceDep,
    card_service: CardServiceDep,
    address_service: AddressServiceDep,
):
    return OrderService(
        session=session,
        buyer_service=buyer_service,
        card_service=card_service,
        address_service=address_service,
    )


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


def get_seller_product_service(
    session: SessionDep,
    seller_service: SellerServiceDep,
    product_service: ProductServiceDep,
):
    return SellerProductService(
        session=session, seller_service=seller_service, product_service=product_service
    )


SellerProductServiceDep = Annotated[
    SellerProductService, Depends(get_seller_product_service)
]


def get_shopping_cart_service(
    session: SessionDep,
    buyer_service: BuyerServiceDep,
    seller_product_service: SellerProductServiceDep,
):
    return InShoppingCartService(
        session=session,
        buyer_service=buyer_service,
        seller_product_service=seller_product_service,
    )


ShoppingCartServiceDep = Annotated[
    InShoppingCartService, Depends(get_shopping_cart_service)
]


def get_wish_list_service(
    session: SessionDep,
    buyer_service: BuyerServiceDep,
    seller_product_service: SellerProductServiceDep,
):
    return InWishListService(
        session=session,
        buyer_service=buyer_service,
        seller_product_service=seller_product_service,
    )


WishListServiceDep = Annotated[InWishListService, Depends(get_wish_list_service)]


def get_product_line_service(
    session: SessionDep,
    buyer_service: BuyerServiceDep,
    order_service: OrderServiceDep,
    seller_product_service: SellerProductServiceDep,
):
    return ProductLineService(
        session=session,
        buyer_service=buyer_service,
        order_service=order_service,
        seller_product_service=seller_product_service,
    )


ProductLineServiceDep = Annotated[ProductLineService, Depends(get_product_line_service)]


def get_refund_product_service(
    session: SessionDep,
    buyer_service: BuyerServiceDep,
    order_service: OrderServiceDep,
    seller_product_service: SellerProductServiceDep,
    product_line_service: ProductLineServiceDep,
):
    return RefundProductService(
        session=session,
        buyer_service=buyer_service,
        order_service=order_service,
        seller_product_service=seller_product_service,
        product_line_service=product_line_service,
    )


RefundProductServiceDep = Annotated[
    RefundProductService, Depends(get_refund_product_service)
]
