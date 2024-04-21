from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.user import UserService
from app.schemas.seller import SellerCreate, SellerUpdate
from app.models.users.types.seller import Seller
from app.crud_repository import CRUDRepository
from app.core.security import get_password_hash
from app.schemas.user import UserUpdate

# from app.models.buyer import Buyer


class SellerRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Seller)
        self._model = Seller

    def get_by_email(self, email: str) -> Seller | None:
        return self._db.query(self._model).filter(self._model.email == email).first()

    def get_by_cif(self, cif: str) -> Seller | None:
        return self._db.query(self._model).filter(self._model.cif == cif).first()


class SellerService:
    def __init__(self, session: Session, user_service: UserService):
        self.session = session
        self.seller_repo = SellerRepository(session=session)
        self.user_service = user_service

    def add(self, seller: SellerCreate) -> Seller:
        if self.user_service.get_by_email(seller.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {seller.email} already exists.",
            )

        if self.seller_repo.get_by_cif(seller.cif):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller with cif {seller.cif} already exists.",
            )

        return self.seller_repo.add(
            Seller(
                **seller.model_dump(exclude={"password"}),
                password=get_password_hash(seller.password),
            )
        )

    def get_by_id(self, seller_id) -> Seller:
        if seller := self.seller_repo.get_by_id(seller_id):
            return seller

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller with id {seller_id} not found.",
        )

    def get_all(self) -> list[Seller]:
        return self.seller_repo.get_all()

    def update(self, seller_id, new_data: SellerUpdate) -> Seller:
        seller = self.get_by_id(seller_id)

        if new_data.email and self.user_service.get_by_email(new_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {new_data.email} already exists.",
            )

        if new_data.cif and self.seller_repo.get_where(
            Seller.id != seller_id, Seller.cif == new_data.cif
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller with CIF {new_data.cif} already exists.",
            )

        common_attributes = {}
        for key in ["email", "name", "surname", "password"]:
            common_attributes[key] = getattr(new_data, key)
            setattr(
                new_data, key, None
            )  # Set attribute to None after fetching its value

        if any(value is not None for value in common_attributes.values()):
            user_update = UserUpdate(**common_attributes)
            self.user_service._user_repository.update(seller, user_update)

        if all(value is None for value in vars(new_data).values()):
            return self.get_by_id(seller_id)

        return self.seller_repo.update(self.get_by_id(seller_id), new_data)

    def delete_by_id(self, seller_id):
        seller = self.seller_repo.get_by_id(seller_id)
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seller with id {seller_id} not found.",
            )
        self.seller_repo.delete_by_id(seller_id)
        self.user_service._user_repository.delete_by_id(seller_id)

    def delete_all(self):
        self.seller_repo.delete_all()
        self.user_service._user_repository.delete_all()
