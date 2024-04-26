from sqlalchemy.orm import Session

from app.service.users.types.user import UserService
from app.models.users.types.buyer import Buyer
from app.crud_repository import CRUDRepository
from app.core.security import get_password_hash
from app.models.users.types.admin import Admin
from app.schemas.users.types.admin import AdminCreate

class AdminService:
    def __init__(self, session: Session, user_service: UserService):
        self.session = session
        self.admin_repo = CRUDRepository(session=session, model=Admin)
        self.user_service = user_service

    def add(self, admin: AdminCreate) -> Buyer:
        
        return self.admin_repo.add(
            Admin(
                **admin.model_dump(exclude={"password"}),
                password=get_password_hash(admin.password),
            )
        )
