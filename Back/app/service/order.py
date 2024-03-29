from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.card import CardService
from app.service.address import AddressService
from app.service.buyer import BuyerService
from app.schemas.order import OrderCreate, OrderUpdate
from app.models.order import Order
from app.crud_repository import CRUDRepository


class OrderService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        card_service: CardService,
        address_service: AddressService,
    ):
        self.session = session
        self.order_repo = CRUDRepository(session=session, model=Order)
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

    def get_buyer_order(self, id_buyer, id_order) -> Order:
        self.buyer_service.get_by_id(id_buyer)
        order = self.get_by_id(id_order)

        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {id_order} does not belong to the buyer with id {id_buyer}.",
            )

        return order

    # def filter_orders(self, *expressions):
    #     try:
    #         return self.order_repo.filter(*expressions)
    #     except Exception as e:
    #         raise e
    #     finally:
    #         self.session.close()

    # Does it make sense to update an order?
    def update(self, order_id, new_data: OrderUpdate) -> Order:
        order = self.get_by_id(order_id)
        return self.order_repo.update(order, new_data)

    def delete_by_id(self, order_id):
        self.get_by_id(order_id)
        self.order_repo.delete_by_id(order_id)

    def delete_all(self):
        self.order_repo.delete_all()
