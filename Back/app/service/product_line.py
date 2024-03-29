from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.product_line import ProductLineCreate
from app.service.buyer import BuyerService
from app.models.product_line import ProductLine
from app.service.order import OrderService
from app.service.seller_product import SellerProductService
from app.crud_repository import CRUDRepository


class ProductLineService:
    def __init__(
        self,
        session: Session,
        buyer_service: BuyerService,
        order_service: OrderService,
        seller_product_service: SellerProductService,
    ):
        self.session = session
        self.product_line_repo = CRUDRepository(session=session, model=ProductLine)
        self.buyer_service = buyer_service
        self.order_service = order_service
        self.seller_product_service = seller_product_service

    def add(self, id_order, id_buyer, product_line: ProductLineCreate) -> ProductLine:
        self.buyer_service.get_by_id(id_buyer)
        order = self.order_service.get_by_id(id_order)

        if order.id_buyer != id_buyer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The order with id {id_order} does not belong to the buyer with id {id_buyer}.",
            )

        seller_product = self.seller_product_service.get_by_id(
            product_line.id_seller_product
        )

        for product_line in order.product_lines:
            if product_line.id_seller_product == seller_product.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product already in order",
                )

        if seller_product.quantity < product_line.quantity:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product quantity exceeds seller's stock",
            )

        if seller_product.price * product_line.quantity != product_line.subtotal:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product subtotal does not match seller's price and quantity",
            )

        product_line = ProductLine(**product_line.model_dump(), id_order=id_order)
        product_line = self.product_line_repo.add(product_line)
        order.product_lines.append(product_line)
        order.total += product_line.subtotal  # type: ignore

        seller_product.quantity -= product_line.quantity  # type: ignore

        self.session.commit()
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

    # def filter_product_lines(self, *expressions):
    #     try:
    #         return self.product_line_repo.filter(*expressions)
    #     except Exception as e:
    #         raise e
    #     finally:
    #         self.session.close()

    # no update method required, once a product line is added to an order it's quantity or anything else should not be changed

    # SHOULD ONLY USE THE METHOD BELOW FOR TESTING
    def delete_by_id(self, product_line_id):
        self.get_by_id(product_line_id)
        self.product_line_repo.delete_by_id(product_line_id)

    def delete_all(self):
        self.product_line_repo.delete_all()
