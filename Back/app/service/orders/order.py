from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.users.types.user import User
from app.schemas.orders.product_line import CompleteProductLine
from app.service.products.product import ProductService
from app.service.products.seller_product import SellerProductService
from app.service.users.card import CardService
from app.service.users.address import AddressService
from app.service.users.types.buyer import BuyerService
from app.schemas.orders.order import OrderCreate, OrderUpdate, CompleteOrder
from app.models.orders.order import Order
from app.crud_repository import CRUDRepository


class OrderRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Order)

    def delete_all_by_buyer_id(self, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()  # type: ignore


class OrderService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        card_service: CardService,
        address_service: AddressService,
        product_service: ProductService,
        seller_product_service: SellerProductService,
    ):
        self.session = session
        self.order_repo = OrderRepository(session=session)
        self.buyer_service = buyer_service
        self.card_service = card_service
        self.address_service = address_service
        self.product_service = product_service
        self.seller_product_service = seller_product_service

    # TODO: it might require additional logic
    # * add eco-points from product lines of the order to the buyer
    # * should the order have already its products on creation?
    def add(self, id_buyer, order: OrderCreate) -> Order:
        self.buyer_service.get_by_id(id_buyer)
        card = self.card_service.get_by_id(order.id_card)

        if card.id_buyer != id_buyer:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The card with id {order.id_card} does not belong to the buyer with id {id_buyer}.",
            )

        address = self.address_service.get_by_id(order.id_address)

        if address.id_buyer != id_buyer:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The address with id {order.id_address} does not belong to the buyer with id {id_buyer}.",
            )

        return self.order_repo.add(Order(**order.model_dump(), id_buyer=id_buyer))

    def add_by_user(self, user: User, order: OrderCreate) -> CompleteOrder:
        self._check_is_buyer(user)
        return self._map_order_to_schema(self.add(user.id, order))

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

    def get_all(self) -> list[Order]:
        return self.order_repo.get_all()

    def get_all_by_buyer_id(self, id_buyer) -> list[Order]:
        self.buyer_service.get_by_id(id_buyer)
        return self.order_repo.get_where(Order.id_buyer == id_buyer)

    def get_buyer_order(self, id_buyer, id_order) -> Order:
        self.buyer_service.get_by_id(id_buyer)
        order = self._get_by_id(id_order)

        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {id_order} does not belong to the buyer with id {id_buyer}.",
            )

        return order

    # Does it make sense to update an order?
    def update(self, order_id, new_data: OrderUpdate) -> Order:
        order = self._get_by_id(order_id)
        return self.order_repo.update(order, new_data)

    def update_by_user(
        self, user: User, order_id, new_data: OrderUpdate
    ) -> CompleteOrder:
        self._check_is_buyer(user)
        self._check_buyer_owns_order(user.id, order_id)
        return self._map_order_to_schema(self.update(order_id, new_data))

    def delete_all_by_user(self, user: User):
        self._check_is_buyer(user)
        self.order_repo.delete_all_by_buyer_id(user.id)

    def delete_one_by_user(self, user: User, order_id):
        self._check_is_buyer(user)
        self._check_buyer_owns_order(user.id, order_id)
        self.delete_by_id(order_id)

    def delete_by_id(self, order_id):
        self.get_by_id(order_id)
        self.order_repo.delete_by_id(order_id)

    def delete_by_buyer_id(self, id_buyer, order_id):
        self.buyer_service.get_by_id(id_buyer)
        order = self.get_by_id(order_id)

        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {order_id} does not belong to the buyer with id {id_buyer}.",
            )

        self.delete_by_id(order_id)

    def delete_all(self):
        self.order_repo.delete_all()

    def delete_all_by_buyer_id(self, id_buyer):
        self.buyer_service.get_by_id(id_buyer)
        self.order_repo.delete_all_by_buyer_id(id_buyer)

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
