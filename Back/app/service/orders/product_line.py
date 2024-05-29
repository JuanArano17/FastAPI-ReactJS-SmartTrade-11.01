from datetime import datetime
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.orders.product_line import CompleteProductLine, ProductLineCreate, ProductLineUpdate
from app.service.users.types.buyer import BuyerService
from app.models.orders.product_line import ProductLine
from app.service.orders.order import OrderService
from app.service.products.seller_product import SellerProductService
from app.crud_repository import CRUDRepository
from app.schemas.products.seller_product import SellerProductUpdate
from app.schemas.orders.order import OrderUpdate
from app.core.enums import OrderState
from app.schemas.products.categories.variations.size import SizeUpdate

class ProductLineRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=ProductLine)
    def add_estimated_date(self, product_line, product_line_update:ProductLineUpdate):
        if product_line == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no product line with this id",
            )
        product_line.estimated_date=product_line_update.estimated_date
        self._db.commit()
        return product_line

    def get_product_lines_by_seller(self,session: Session, seller_id: int):
        from app.models.products.seller_product import SellerProduct
        from app.models.orders.order import Order
        stmt = (
            select(ProductLine)
            .join(SellerProduct, SellerProduct.id == ProductLine.id_seller_product)
            .join(Order, Order.id==ProductLine.id_order)
            .filter(SellerProduct.id_seller == seller_id)
            .filter(Order.state==OrderState.CONFIRMED)
        )
        return session.execute(stmt).scalars().all()

class ProductLineService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        order_service: OrderService,
        seller_product_service: SellerProductService,
    ):
        self.session = session
        self.product_line_repo = ProductLineRepository(session=session)
        self.buyer_service = buyer_service
        self.order_service = order_service
        self.seller_product_service = seller_product_service

    def add(self, id_order, id_buyer, product_line: ProductLineCreate) -> ProductLine:
        self.buyer_service.get_by_id(id_buyer)
        order = self.order_service.order_repo.get_by_id(id_order)
        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {id_order} does not belong to the buyer with id {id_buyer}.",
            )

        seller_product = self.seller_product_service.get_by_id(
            product_line.id_seller_product
        )

        original_product_line = product_line
        for product_line in order.product_lines:
            if product_line.id_seller_product == seller_product.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product already in order",
                )
        product_line = original_product_line
        if seller_product.quantity < product_line.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product quantity exceeds seller's stock",
            )

        product_line_subtotal = Decimal(product_line.subtotal).quantize(Decimal("0.01"))
        seller_product_price = Decimal(seller_product.price).quantize(Decimal("0.01"))
        calculated_subtotal = (
            seller_product_price * Decimal(product_line.quantity)
        ).quantize(Decimal("0.01"))

        if product_line_subtotal != calculated_subtotal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product subtotal does not match seller's price and quantity",
            )

        product_line = ProductLine(**product_line.model_dump(), id_order=id_order)
        order.total += Decimal(product_line.subtotal)

        if seller_product.sizes == []:
            print(
                f"seller product - product line quantity: {seller_product.quantity} - {product_line.quantity}\n\n\n\n"
            )
            seller_product_update = SellerProductUpdate(
                quantity=seller_product.quantity - product_line.quantity
            )
            self.seller_product_service.update(seller_product.id, seller_product_update)
        else:
            pass  
        product_line = self.product_line_repo.add(product_line)
        return product_line

    def get_by_id(self, product_line_id) -> ProductLine:
        if product_line := self.product_line_repo.get_by_id(product_line_id):
            return product_line

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product Line with id {product_line_id} not found.",
        )

    def get_all(self) -> list[ProductLine]:
        return self.product_line_repo.get_all()

    def get_all_by_order_id(self, order_id) -> list[ProductLine]:
        return self.product_line_repo.get_where(ProductLine.id_order == order_id)
    
    def get_all_by_seller_id(self, seller_id) -> list[ProductLine]:
        seller=self.seller_product_service.seller_service.get_by_id(seller_id)
        self._check_is_seller(seller)
        product_lines=self.product_line_repo.get_product_lines_by_seller(self.session,seller_id)
        complete_product_lines=[]
        for product_line in product_lines:
            seller_product = self.seller_product_service.get_by_id(
                    product_line.id_seller_product
                )
            product = self.seller_product_service.product_service.get_by_id(seller_product.id_product)
            if product_line.id_size:
                complete_product_lines.append(
                        CompleteProductLine(
                            **product_line.__dict__,
                            name=product.name,
                            description=product.description,
                            category=product.category,
                            refund_products=product_line.refund_products,
                            size=self.seller_product_service.size_repo.get_by_id(product_line.id_size),
                        )
                    )
            else:
                complete_product_lines.append(
                        CompleteProductLine(
                            **product_line.__dict__,
                            name=product.name,
                            description=product.description,
                            category=product.category,
                            refund_products=product_line.refund_products)
                    )
        return complete_product_lines

    def add_estimated_date(self, product_line_id, user, estimated_date:ProductLineUpdate):
        product_line=self.get_by_id(product_line_id)
        seller_product=self.seller_product_service.get_by_id(product_line.id_seller_product)
        if user.id!=seller_product.id_seller:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This product line does not belong to the user",
            )
        if product_line.estimated_date!=None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This product line already has an estimated date",
            )
        ship=True
        max=datetime.now().date()
        new_product_line=self.product_line_repo.add_estimated_date(product_line, estimated_date)
        order=self.order_service.order_repo.get_by_id(product_line.id_order)
        buyer=self.buyer_service.get_by_id(order.id_buyer)
        for product_line in order.product_lines:
            if product_line.estimated_date==None:
                ship=False
                break
            if(product_line.estimated_date>max):
                max=product_line.estimated_date
        if ship:    
            for product_line in order.product_lines:
                print(product_line)
            data=OrderUpdate(estimated_date=max)

            print("---")
            for product_line in order.product_lines:
                print(product_line)
            self.order_service.ship_confirmed_order(buyer,data,order.id)
        return new_product_line

    def _check_is_seller(self, user):
        if not str(user.type) == "Seller":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Users of type {user.type} do not have product lines.",
            )
    
    # SHOULD ONLY USE THE METHOD BELOW FOR TESTING
    def delete_by_id(self, product_line_id):
        product_line=self.get_by_id(product_line_id)
        order=self.order_service.get_by_id(product_line.order.id)
        seller_product=self.seller_product_service.get_by_id(product_line.id_seller_product)

        order.total -= float(product_line.subtotal)

        if seller_product.sizes == []:
            seller_product_update = SellerProductUpdate(
                quantity=seller_product.quantity + product_line.quantity
            )
        else:
            old_size=self.seller_product_service.size_repo.get_by_id(product_line.id_size)
            old_quantity=old_size.quantity
            size=SizeUpdate(size=old_size.size, quantity=old_quantity+product_line.quantity)
            seller_product_update = SellerProductUpdate(
                        sizes=[size]
                    )
        self.order_service.seller_product_service.update(seller_product.id, seller_product_update)
        
        self.product_line_repo.delete_by_id(product_line_id)

    def delete_all(self):
        self.product_line_repo.delete_all()
