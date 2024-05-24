from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.core.enums import OrderState
from app.models.orders.product_line import ProductLine
from app.models.users.types.user import User
from app.models.orders.order import Order
from app.service.users.in_shopping_cart import InShoppingCartService
from app.service.products.product import ProductService
from app.service.products.seller_product import SellerProductService
from app.service.users.card import CardService
from app.service.users.address import AddressService
from app.service.users.types.buyer import BuyerService
from app.schemas.orders.product_line import CompleteProductLine
from app.schemas.orders.order import ConfirmOrder, CompleteOrder, OrderCreate
from app.crud_repository import CRUDRepository


class OrderRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Order)

    def delete_all_by_buyer_id(self, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()

    def delete_where(self, *conditions):
        self._db.query(self._model).filter(*conditions).delete()


class OrderService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        card_service: CardService,
        address_service: AddressService,
        product_service: ProductService,
        seller_product_service: SellerProductService,
        shopping_cart_service: InShoppingCartService,
    ):
        self.session = session
        self.order_repo = OrderRepository(session=session)
        self.buyer_service = buyer_service
        self.card_service = card_service
        self.address_service = address_service
        self.product_service = product_service
        self.seller_product_service = seller_product_service
        self.shopping_cart_service = shopping_cart_service

    def create_from_shopping_cart(self, user: User) -> Order:
        self._check_is_buyer(user)
        shopping_cart = self.shopping_cart_service.get_by_user(user)

        if shopping_cart == []:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create an order from the user's shopping cart if it is empty.",
            )

        self.order_repo.delete_where(
            Order.state == OrderState.PENDING, Order.id_buyer == user.id
        )
        order = self.order_repo.add(Order(id_buyer=user.id, total=0))

        for item in shopping_cart:
            subtotal = item.seller_product.price * item.quantity
            order.product_lines.append(
                ProductLine(
                    id_seller_product=item.seller_product.id,
                    quantity=item.quantity,
                    subtotal=subtotal,
                )
            )
            order.total += Decimal(subtotal)

        self.session.commit()
        return order

    def confirm_pending_order(self, user: User, data: ConfirmOrder) -> Order:
        self._check_is_buyer(user)
        order = self.order_repo.get_where(
            Order.state == OrderState.PENDING, Order.id_buyer == user.id
        )[0]

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User {user.email} does not have a pending order.",
            )

        # Checking if this user owns the card and address sent in the request
        self.card_service.get_one_by_user(user, data.id_card)
        self.address_service.get_one_by_user(user, data.id_address)

        order.state = OrderState.CONFIRMED
        order.order_date = datetime.now()
        order.id_card = data.id_card
        order.id_address = data.id_address

        for product_line in order.product_lines:
            product = self.seller_product_service.get_by_id(
                product_line.id_seller_product
            ).product
            product.stock -= product_line.quantity
            product_line.seller_product.stock -= product_line.quantity

        self.shopping_cart_service.delete_all_by_user(user)

        self.session.commit()
        return order

    def get_by_id(self, order_id) -> CompleteOrder:
        order = self.order_repo.get_by_id(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found.",
            )

        return self._map_order_to_schema(order)

    def _get_by_id(self, order_id) -> Order:
        if order := self.order_repo.get_by_id(order_id):
            return order

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found.",
        )

    def get_one_by_user(self, user: User, order_id) -> CompleteOrder:
        self._check_is_buyer(user)
        self._check_buyer_owns_order(user.id, order_id)
        return self.get_by_id(order_id)

    def get_all_by_user(self, user: User) -> list[CompleteOrder]:
        self._check_is_buyer(user)
        return [
            self._map_order_to_schema(order)
            for order in self.get_all_by_buyer_id(user.id)
        ]

    def get_all_by_buyer_id(self, id_buyer) -> list[Order]:
        self.buyer_service.get_by_id(id_buyer)
        return self.order_repo.get_where(Order.id_buyer == id_buyer)

    def delete_all(self):
        self.order_repo.delete_all()

    def populate(self, id_buyer: int, order: OrderCreate) -> Order:
        order = Order(id_buyer=id_buyer, **order.model_dump())
        self.order_repo.add(order)
        return order

    def _map_order_to_schema(self, order: Order) -> CompleteOrder:
        complete_product_lines = []

        for product_line in order.product_lines:
            seller_product = self.seller_product_service.get_by_id(
                product_line.id_seller_product
            )
            product = self.product_service.get_by_id(seller_product.id_product)
            complete_product_lines.append(
                CompleteProductLine(
                    **product_line.__dict__,
                    name=product.name,
                    description=product.description,
                    category=product.category,
                    refund_products=product_line.refund_products,
                )
            )

        del order.product_lines

        return CompleteOrder(
            **order.__dict__,
            product_lines=complete_product_lines,
        )

    def _check_is_buyer(self, user: User):
        if not str(user.type) == "Buyer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Users of type {user.type} do not have cards.",
            )

    def _check_buyer_owns_order(self, buyer_id, order_id):
        if not self.order_repo.get_where(
            Order.id == order_id, Order.id_buyer == buyer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found for buyer with id {buyer_id}.",
            )
