from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.core.enums import OrderState, OrderType
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
from app.schemas.orders.order import CompleteOrder, ConfirmOrder, OrderCreate, OrderUpdate
from app.crud_repository import CRUDRepository
from app.schemas.products.categories.variations.size import SizeUpdate
from app.schemas.products.seller_product import SellerProductUpdate

class OrderStateBase:
    def __init__(self, order, order_service):
        self.order = order
        self.order_service = order_service

    def validate(self, order_update):
        raise NotImplementedError("Must implement in subclass")

    def apply(self, user, order_update):
        pass

class ConfirmedState(OrderStateBase):
    def validate(self, order_update):
        if order_update.estimated_date is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="estimated_date cannot be null in state SHIPPED."
                )
        
        if self.order.state!=OrderState.CONFIRMED:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="order state must be confirmed to be in the confirmed state"
            )
        
        if order_update.id_address is not None or order_update.id_card is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_address and id_card cannot be changed after confirmation."
            )

    def apply(self, user, order_update):
            self.order.state = OrderState.SHIPPED
            if(self.order.type==OrderType.STANDARD):
                order_update.estimated_date+=timedelta(days=2)
            updated_order=self.order_service.order_repo.update(self.order, order_update)
            return updated_order

class ShippedState(OrderStateBase):
    def validate(self, order_update):
        if self.order.state!=OrderState.SHIPPED:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="shipped state must be shipped to be in the shipped state"
            )

        if order_update.id_address is not None or order_update.id_card is not None or order_update.estimated_date is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_address and id_card and estimated date cannot be changed after shipping."
            )

    def apply(self,user,order_update):
        self.order.state = OrderState.DELIVERED
        if(datetime.now().date()>self.order.estimated_date):
            return self.order_service.order_repo.update(self.order, OrderUpdate())

class DeliveredState(OrderStateBase):
    def validate(self, order_update):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot transition from DELIVERED."
        )

    def apply(self, user, order_update):
        pass

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

    def populate(self, id_buyer: int, order: OrderCreate) -> Order:
        order = Order(id_buyer=id_buyer, **order.model_dump())
        self.order_repo.add(order)
        return order

    def create_from_shopping_cart(self, user: User, order_create:ConfirmOrder) -> Order:
        self._check_is_buyer(user)
        shopping_cart = self.shopping_cart_service.get_by_user(user)

        if shopping_cart == []:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create an order from the user's shopping cart if it is empty.",
            )
        self.card_service.get_one_by_user(user, order_create.id_card)
        self.address_service.get_one_by_user(user, order_create.id_address)
        estimated_date=datetime.now().date()+timedelta(weeks=1)
        if(order_create.type==OrderType.STANDARD or order_create.type==None):
            estimated_date+=timedelta(days=2)
        order = Order(total=0, order_date=datetime.now(), id_buyer=user.id, state=OrderState.CONFIRMED, **order_create.model_dump(), estimated_date=estimated_date)
        if order.type==OrderType.PREMIUM:
            order.total=5
        order.id_address=order_create.id_address
        order.id_card=order_create.id_card
        order=self.order_repo.add(order)
        self.shopping_cart_service.delete_all_by_user(user)


        for item in shopping_cart:
            subtotal = item.seller_product.price * item.quantity + item.seller_product.shipping_costs
            if item.size==None:
                id_size=None
            else:
                id_size=item.size.id
            order.product_lines.append(
                ProductLine(
                    id_seller_product=item.seller_product.id,
                    quantity=item.quantity,
                    subtotal=subtotal,
                    id_size=id_size
                )
            )
            order.total += Decimal(subtotal)

        for product_line in order.product_lines:
            product = self.seller_product_service.get_by_id(
                product_line.id_seller_product
            ).product
            seller_product=self.seller_product_service.get_by_id(product_line.id_seller_product)
            if seller_product.sizes==None or seller_product.sizes==[]:
                seller_product_update = SellerProductUpdate(
                quantity=seller_product.quantity - product_line.quantity
                )
                self.seller_product_service.update(seller_product.id, seller_product_update)
            else:
                old_size=self.seller_product_service.size_repo.get_by_id(product_line.id_size)
                old_quantity=old_size.quantity
                size=SizeUpdate(size=old_size.size, quantity=old_quantity-product_line.quantity)
                seller_product_update = SellerProductUpdate(
                    sizes=[size]
                )
                self.seller_product_service.update(seller_product.id, seller_product_update)
        order=self._get_by_id(order.id)
        return order
    
    def get_state_instance(self, state, order):
        if(state==OrderState.CONFIRMED):
            return ConfirmedState(order, self)
        elif(state==OrderState.SHIPPED):
            return ShippedState(order, self)
        elif(state==OrderState.DELIVERED):
            return DeliveredState(order, self)
        else:
            raise ValueError("This state does not exist")
        
    def update_order(self, user: User, data: OrderUpdate, id_order:int, state) -> Order:
        self._check_is_buyer(user)
        orders = self.order_repo.get_where(
            Order.state == state, Order.id_buyer == user.id, Order.id==id_order
        )

        if orders is None or orders==[]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user.email} does not have a confirmed order with this id.",
            )
        else:
            order=orders[0]
        state_instance = self.get_state_instance(state, order)
        state_instance.validate(data)
        return state_instance.apply(user, data)
    
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
        for order in self.get_all_by_buyer_id(user.id):
            if(order.estimated_date and order.state== OrderState.SHIPPED):
                if datetime.now().date()>=order.estimated_date:
                    self.update_order(user, OrderUpdate(), order.id, OrderState.SHIPPED)
        return [
            self._map_order_to_schema(order)
            for order in self.get_all_by_buyer_id(user.id)
        ]

    def get_all_by_buyer_id(self, id_buyer) -> list[Order]:
        self.buyer_service.get_by_id(id_buyer)
        return self.order_repo.get_where(Order.id_buyer == id_buyer)

    def delete_all(self):
        self.order_repo.delete_all()

    def _map_order_to_schema(self, order: Order) -> CompleteOrder:
        complete_product_lines = []

        for product_line in order.product_lines:
            seller_product = self.seller_product_service.get_by_id(
                product_line.id_seller_product
            )
            product = self.product_service.get_by_id(seller_product.id_product)
            if product_line.id_size:
                complete_product_lines.append(
                    CompleteProductLine(
                        **product_line.__dict__,
                        name=product.name,
                        description=product.description,
                        category=product.category,
                        refund_products=product_line.refund_products,
                        size=self.seller_product_service.size_repo.get_by_id(product_line.id_size)
                        #estimated_date=product_line.estimated_date
                    )
                )
            else:
                complete_product_lines.append(
                    CompleteProductLine(
                        **product_line.__dict__,
                        name=product.name,
                        description=product.description,
                        category=product.category,
                        refund_products=product_line.refund_products,
                        size=self.seller_product_service.size_repo.get_by_id(product_line.id_size)
                        #estimated_date=product_line.estimated_date
                    )
                )


        del order.product_lines

        return CompleteOrder(
            **order.__dict__,
            product_lines=complete_product_lines
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
