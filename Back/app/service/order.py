from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.card import CardService
from app.service.address import AddressService
from app.service.buyer import BuyerService
from app.schemas.order import OrderCreate, OrderUpdate
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
    ):
        self.session = session
        self.order_repo = OrderRepository(session=session)
        self.buyer_service = buyer_service
        self.card_service = card_service
        self.address_service = address_service

    # TODO: it might require additional logic
    # * add eco-points from product lines of the order to the buyer
    # * should the order have already its products on creation?
    def add(self, id_buyer: int, order: OrderCreate) -> Order:
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

    def get_by_id(self, order_id) -> Order:
        if order := self.order_repo.get_by_id(order_id):
            return order

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found.",
        )

    def get_all(self) -> list[Order]:
        return self.order_repo.get_all()

    def get_all_by_buyer_id(self, id_buyer) -> list[Order]:
        self.buyer_service.get_by_id(id_buyer)
        return self.order_repo.get_where(Order.id_buyer == id_buyer)

    def get_buyer_order(self, id_buyer, id_order) -> Order:
        self.buyer_service.get_by_id(id_buyer)
        order = self.get_by_id(id_order)

        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {id_order} does not belong to the buyer with id {id_buyer}.",
            )

        return order

    # Does it make sense to update an order?
    def update(self, order_id, new_data: OrderUpdate) -> Order:
        order = self.get_by_id(order_id)
        return self.order_repo.update(order, new_data)

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
