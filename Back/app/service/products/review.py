from sqlalchemy import select
from app.models.users.types.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.products.seller_product import SellerProductService
from app.service.users.types.buyer import BuyerService
from app.crud_repository import CRUDRepository
from app.models.products.review import Review
from app.schemas.products.review import CompleteReview, ReviewCreate
from app.schemas.users.types.buyer import Buyer
from app.core.enums import OrderState


class ReviewRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Review)
        self._model = Review

    def get_by_id_buyer(self, *, id_buyer) -> list[Review]:
        return (
            self._db.query(self._model).filter(self._model.id_buyer == id_buyer).all()
        )

    def delete_by_id_buyer(self, *, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()
        self._db.commit()

    def get_repeat_review(self, id_buyer, id_seller_product):
        return self.get_where(self._model.id_buyer==id_buyer, self._model.id_seller_product==id_seller_product)

    def get_seller_product_by_buyer(self,session: Session, buyer_id: int):
        from app.models.orders.order import Order
        from app.models.orders.product_line import ProductLine
        from app.models.products.seller_product import SellerProduct
        from app.schemas.users.types.buyer import Buyer
        stmt = (
            select(SellerProduct)
            .join(ProductLine, ProductLine.id_seller_product == SellerProduct.id)
            .join(Order, Order.id == ProductLine.id_order)
            .filter(Order.id_buyer == buyer_id)
            .filter(Order.state==OrderState.DELIVERED)
        )
        return session.execute(stmt).scalars().all()
    
class ReviewService:
    def __init__(
        self,
        session: Session,
        seller_product_service: SellerProductService,
        buyer_service: BuyerService,
    ):
        self.session = session
        self.review_repo = ReviewRepository(session=session)
        self.seller_product_service = seller_product_service
        self.buyer_service = buyer_service

    def add(self, id_buyer, review: ReviewCreate) -> Review:
        if self.review_repo.get_where(
            Review.id_buyer == id_buyer,
            Review.id_seller_product == review.id_seller_product,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A review was already made by this user for this seller product",
            )
        
        if self.seller_product_service.get_by_id(review.id_seller_product) not in self.get_seller_product_by_buyer(id_buyer):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The buyer must have purchased AND received the product to review it",
            )
        
        self.buyer_service.get_by_id(id_buyer)
        self.seller_product_service.get_by_id(review.id_seller_product)

        review_item = Review(**review.model_dump(), id_buyer=id_buyer)

        reviews=self.review_repo.get_where(
            Review.id_seller_product == review.id_seller_product,
        )

        seller_product=self.seller_product_service.get_by_id(review.id_seller_product)
        if reviews==[]:
             seller_product.stars=review_item.stars
        else:
            reviews.append(review_item)
            total_stars=0
            number_of_reviews=0
            for review in reviews:
                number_of_reviews+=1
                total_stars+=review.stars
            seller_product.stars=round(total_stars/number_of_reviews,1)

        review_item=self.review_repo.add(review_item)
        return review_item

    def add_by_user(
        self, user: User, review: ReviewCreate
    ) -> CompleteReview:
        buyer = self.buyer_service.get_by_id(user.id)
        review = self.add(id_buyer=buyer.id, review=review)
        seller_product = self.seller_product_service.get_by_id(
            review.id_seller_product
        )
        complete_seller_product = (
            self.seller_product_service.map_seller_product_to_read_schema(
                seller_product
            )
        )
        return Review(
            **review.__dict__, seller_product=complete_seller_product, buyer=buyer
        )

    def get_by_id(self, id_review) -> Review:
        if review_item := self.review_repo.get_by_id(
            id=id_review
        ):
            return review_item

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review item not found",
        )

    def get_all(self) -> list[Review]:
        return self.review_repo.get_all()

    def get_all_by_buyer(self, id_buyer) -> list[Review]:
        return self.review_repo.get_where(Review.id_buyer == id_buyer)
    
    def get_all_by_seller_product(self, id_seller_product) -> list[CompleteReview]:
        reviews=self.review_repo.get_where(Review.id_seller_product == id_seller_product)
        review_items=[]
        for item in reviews:
            seller_product = self.seller_product_service.get_by_id(
                item.id_seller_product
            )
            complete_seller_product = (
                self.seller_product_service.map_seller_product_to_read_schema(
                    seller_product
                )
            )
            buyer=self.buyer_service.get_by_id(item.id_buyer)
            buyer=Buyer(email=buyer.email, name=buyer.name, surname=buyer.surname, birth_date=buyer.birth_date, eco_points=buyer.eco_points, dni=buyer.dni, billing_address=buyer.billing_address, payment_method=buyer.payment_method, profile_picture=buyer.profile_picture, id=buyer.id, type=buyer.type, addresses=buyer.addresses, in_shopping_cart=buyer.in_shopping_carts, in_wish_list=buyer.in_wish_lists, cards=buyer.cards, orders=buyer.orders)
            complete_review=CompleteReview(
                    id=item.id,id_buyer=item.id_buyer, stars=item.stars, comment=item.comment, buyer=buyer,  seller_product=complete_seller_product
                )
            review_items.append(
                complete_review
            )
            

        return review_items 

    def get_all_by_user(self, user: User) -> list[Review]:
        buyer = self.buyer_service.get_by_id(user.id)
        reviews = []

        for item in self.get_all_by_buyer(buyer.id):
            seller_product = self.seller_product_service.get_by_id(
                item.id_seller_product
            )
            complete_seller_product = (
                self.seller_product_service.map_seller_product_to_read_schema(
                    seller_product
                )
            )
            reviews.append(
                CompleteReview(
                    **item.__dict__, seller_product=complete_seller_product, buyer=buyer #wrong
                )
            )

        return reviews

    def delete_by_id(self,id_buyer,id_review):
        reviews=self.get_all_by_buyer(id_buyer)
        review=self.get_by_id(id_review)
        if review in reviews:
            self.get_by_id(id_review)
            self.review_repo.delete_by_id(
                id_review
            )
        else:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The review that you are trying to delete does not belong to the buyer",
        )

    def delete_all(self):
        self.review_repo.delete_all()

    def get_by_id_buyer(self, id_buyer) -> list[Review]:
        return self.review_repo.get_by_id_buyer(id_buyer=id_buyer)

    def delete_by_id_buyer(self, id_buyer):
        return self.review_repo.delete_by_id_buyer(id_buyer=id_buyer)

    def delete_all_by_user(self, user: User):
        buyer = self.buyer_service.get_by_id(user.id)
        self.delete_by_id_buyer(buyer.id)

    def get_seller_product_by_buyer(self, buyer_id):
        return self.review_repo.get_seller_product_by_buyer(self.session, buyer_id)
    #def delete_one_by_user(self, id_review):
    #    self.delete_by_id(id_review)
