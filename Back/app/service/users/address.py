from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.users.address import AddressCreate, AddressUpdate
from app.models.users.types.user import User
from app.models.users.address import Address
from app.crud_repository import CRUDRepository
from app.service.users.types.buyer import BuyerService


class AddressRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Address)
        self._model = Address

    def get_by_id_buyer(self, id_buyer) -> list[Address]:
        return (
            self._db.query(self._model).filter(self._model.id_buyer == id_buyer).all()
        )

    def delete_by_id_buyer(self, id_buyer):
        self._db.query(self._model).filter(self._model.id_buyer == id_buyer).delete()
        self._db.commit()

    def get_default(self, id_buyer) -> Address:
        return (
            self._db.query(self._model)
            .filter(self._model.id_buyer == id_buyer, self._model.default == True)
            .first()
        )


class AddressService:
    def __init__(self, session: Session, buyer_service: BuyerService):
        self.session = session
        self.buyer_service = buyer_service
        self.address_repo = AddressRepository(session=session)

    def _update_old_default_address(self, id_buyer):
        default_address = self.address_repo.get_where(
            Address.default == True, Address.id_buyer == id_buyer
        )
        if default_address:
            self.address_repo.update(default_address[0], AddressUpdate(default=False))

    def add(self, id_buyer, address: AddressCreate) -> Address:
        self.buyer_service.get_by_id(id_buyer)

        if address.default:
            self._update_old_default_address(id_buyer)

        address_obj = Address(**address.model_dump(), id_buyer=id_buyer)
        address_obj = self.address_repo.add(address_obj)
        return address_obj

    def add_by_user(self, user: User, address: AddressCreate) -> Address:
        self._check_is_buyer(user)
        return self.add(user.id, address)

    def get_all(self) -> list[Address]:
        return self.address_repo.get_all()

    def get_default(self, id_buyer) -> Address | None:
        return self.address_repo.get_default(id_buyer=id_buyer)

    def get_all_by_user(self, user: User) -> list[Address]:
        self._check_is_buyer(user)
        return self.address_repo.get_by_id_buyer(user.id)

    def get_by_id(self, id) -> Address:
        if address := self.address_repo.get_by_id(id):
            return address

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id {id} not found.",
        )

    def get_by_id_buyer(self, id_buyer) -> list[Address]:
        return self.address_repo.get_by_id_buyer(id_buyer=id_buyer)

    def get_one_by_user(self, user: User, address_id) -> Address:
        self._check_is_buyer(user)
        address = self.get_by_id(address_id)
        if address.id_buyer != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address does not belong to the user.",
            )
        return address

    def get_default_by_user(self, user: User) -> Address:
        self._check_is_buyer(user)
        return self.address_repo.get_default(user.id)

    def update(self, address_id, new_data: AddressUpdate) -> Address:
        address = self.get_by_id(address_id)

        if new_data.default:
            self._update_old_default_address(address.id_buyer)

        return self.address_repo.update(address, new_data)

    def update_by_user(
        self, user: User, address_id, new_data: AddressUpdate
    ) -> Address:
        self._check_is_buyer(user)
        address = self.get_one_by_user(user, address_id)
        if new_data.default:
            self._update_old_default_address(address.id_buyer)
        return self.address_repo.update(address, new_data)

    def delete_by_id(self, address_id):
        self.get_by_id(address_id)
        self.address_repo.delete_by_id(address_id)

    def delete_all(self):
        self.address_repo.delete_all()

    def delete_all_by_user(self, user: User):
        self._check_is_buyer(user)
        self.address_repo.delete_by_id_buyer(user.id)

    def delete_one_by_user(self, user: User, address_id):
        self._check_is_buyer(user)
        address = self.get_one_by_user(user, address_id)
        self.address_repo.delete_by_id(address.id)

    def _check_is_buyer(self, user: User):
        if str(user.type) != "Buyer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a buyer.",
            )
