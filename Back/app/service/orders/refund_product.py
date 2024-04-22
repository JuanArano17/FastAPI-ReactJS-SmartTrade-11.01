from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.users.types.buyer import BuyerService
from app.schemas.orders.refund_product import RefundProductCreate
from app.models.orders.refund_product import RefundProduct
from app.service.orders.order import OrderService
from app.service.orders.product_line import ProductLineService
from app.crud_repository import CRUDRepository
from app.service.products.seller_product import SellerProductService


class RefundProductService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        order_service: OrderService,
        seller_product_service: SellerProductService,
        product_line_service: ProductLineService,
    ):
        self.session = session
        self.refund_product_repo = CRUDRepository(session=session, model=RefundProduct)
        self.buyer_service = buyer_service
        self.order_service = order_service
        self.seller_product_service = seller_product_service
        self.product_line_service = product_line_service

    # buyers/{id_buyer}/orders/{id_order}/product_lines/{id_product_line}/refund_products
    def add(
        self, id_buyer, id_order, id_product_line, refund_product: RefundProductCreate
    ) -> RefundProduct:
        order = self.order_service.get_buyer_order(id_buyer, id_order)
        product_line = self.product_line_service.get_by_id(id_product_line)
        # seller_product=self.seller_product_service.get_by_id(product_line.id_seller_product)
        if product_line.id_order != id_order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The product line with id {id_product_line} does not belong to the order with id {id_order}.",
            )

        if refund_product.refund_date.date() < order.order_date:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refund date must be greater than order date",
            )

        if refund_product.refund_date.date() > order.order_date + timedelta(days=30):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refund date must be within 30 days of order date",
            )

        if refund_product.quantity > product_line.quantity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refund quantity cannot be greater than product line quantity",
            )

        refund_product = RefundProduct(
            **refund_product.model_dump(), id_product_line=id_product_line
        )

        product_line.quantity -= refund_product.quantity  # type: ignore
        # must update seller product quantity whenever refund is made
        # product_line.subtotal=seller_product.price*product_line.quantity
        # seller_product.quantity += refund_product.quantity
        refund_product = self.refund_product_repo.add(refund_product)
        return refund_product

    def get_by_id(self, refund_product_id) -> RefundProduct:
        if refund_product := self.refund_product_repo.get_by_id(refund_product_id):
            return refund_product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Refund product with id {refund_product_id} not found.",
        )

    def get_all(self) -> list[RefundProduct]:
        return self.refund_product_repo.get_all()

    def get_all_by_buyer_order(self, id_buyer, id_order) -> list[RefundProduct]:
        self.buyer_service.get_by_id(id_buyer)
        order = self.order_service.get_buyer_order(id_buyer, id_order)
        return self.refund_product_repo.get_where(order.id == RefundProduct.id_order)

    def get_all_by_product_line(
        self, id_buyer, id_order, id_product_line
    ) -> list[RefundProduct]:
        self.buyer_service.get_by_id(id_buyer)
        order = self.order_service.get_buyer_order(id_buyer, id_order)
        product_line = self.product_line_service.get_by_id(id_product_line)
        return self.refund_product_repo.get_where(
            RefundProduct.id_order == order.id,
            RefundProduct.id_product_line == product_line.id,
        )

    # no update method because we don't update a refund's details after it's made

    # buyers/{id_buyer}/orders/{id_order}/product_lines/{id_product_line}/refund_products/{refund_product_id}
    def delete_by_id(self, id_buyer, id_order, id_product_line, refund_product_id):
        self.buyer_service.get_by_id(id_buyer)
        order = self.order_service.get_buyer_order(id_buyer, id_order)
        product_line = self.product_line_service.get_by_id(id_product_line)
        # seller_product=self.seller_product_service.get_by_id(product_line.id_seller_product)

        if product_line.id_order != id_order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The product line with id {id_product_line} does not belong to the order with id {id_order}.",
            )

        refund_product = self.get_by_id(refund_product_id)

        if refund_product.id_product_line != product_line.id:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The refund product with id {refund_product_id} does not belong to the product line with id {id_product_line}.",
            )

        if product_line.id_order != order.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The refund product with id {refund_product_id} does not belong to the order with id {id_order}.",
            )

        product_line.quantity += refund_product.quantity  # type: ignore
        # seller_product.quantity -= refund_product.quantity
        self.refund_product_repo.delete_by_id(refund_product_id)

    def delete_by_product_line(self, id_buyer, id_order, id_product_line):
        refund_products = self.get_all_by_product_line(
            id_buyer, id_order, id_product_line
        )
        for refund_product in refund_products:
            self.refund_product_repo.delete_by_id(refund_product.id)
