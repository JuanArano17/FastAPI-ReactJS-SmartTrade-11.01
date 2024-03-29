from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.seller import SellerCreate, SellerUpdate
from app.models.seller import Seller
from app.crud_repository import CRUDRepository
#from models.buyer import Buyer

class SellerRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Seller)
        self._model = Seller

    def get_by_email(self, email: str) -> Seller | None:
        return self._db.query(self._model).filter(self._model.email == email).first()
    
    def get_by_cif(self, cif: str) -> Seller | None:
        return self._db.query(self._model).filter(self._model.cif == cif).first()

class SellerService:
    def __init__(self, session: Session):
        self.session = session
        self.seller_repo = SellerRepository(session=session)

    def add(self, seller: SellerCreate) -> Seller:

        if self.seller_repo.get_by_email(seller.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with email {seller.email} already exists.",
            )
        
        if self.seller_repo.get_by_cif(seller.cif):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Buyer with email {seller.cif} already exists.",
            )
        
       # buyer_repo=CRUDRepository(self.session,Buyer).first()
       # if buyer_repo.filter(Buyer.email==seller.email):
       #     raise HTTPException(
       #         status_code=status.HTTP_400_BAD_REQUEST,
       #         detail=f"User with email {seller.email} already exists.",
       #     )
        
        return self.seller_repo.add(Seller(**seller.model_dump()))

    def get_by_id(self, seller_id) -> Seller:
        if seller := self.seller_repo.get_by_id(seller_id):
            return seller

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller with id {seller_id} not found.",
        )

    def get_all(self) -> list[Seller]:
        return self.seller_repo.get_all()

    # def filter_sellers(self, *expressions):
    #     try:
    #         return self.seller_repo.filter(*expressions)
    #     except Exception as e:
    #         raise e
    #     finally:
    #         self.session.close()

    def update(self, seller_id, new_data: SellerUpdate) -> Seller:
        seller = self.get_by_id(seller_id)

        if new_data.email and self.seller_repo.get_where(
            Seller.id != seller_id, Seller.email == new_data.email
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller with email {new_data.email} already exists.",
            )

        if new_data.cif and self.seller_repo.get_where(
            Seller.id != seller_id, Seller.cif == new_data.cif
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller with CIF {new_data.cif} already exists.",
            )
        
       # buyer_repo=CRUDRepository(self.session,Buyer)
       # if new_data.email and buyer_repo.filter(Buyer.email==seller.email).first():
       #     raise HTTPException(
       #         status_code=status.HTTP_400_BAD_REQUEST,
       #         detail=f"User with email {new_data.email} already exists.",
       #     )


        return self.seller_repo.update(seller, new_data)

    def delete_by_id(self, seller_id):
        self.get_by_id(seller_id)
        self.seller_repo.delete_by_id(seller_id)

    def delete_all(self):
        self.seller_repo.delete_all()
