from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.service.users.types.user import UserService
from app.crud_repository import CRUDRepository
from app.core.security import get_password_hash
from app.models.users.types.admin import Admin
from app.schemas.users.types.admin import AdminCreate


class AdminService:
    def __init__(self, session: Session, user_service: UserService):
        self.session = session
        self.admin_repo = CRUDRepository(session=session, model=Admin)
        self.user_service = user_service

    def add(self, admin: AdminCreate) -> Admin:
        if self.user_service.get_by_email(email=admin.email, exception=False):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {admin.email} already exists.",
            )

        return self.admin_repo.add(
            Admin(
                **admin.model_dump(exclude={"password"}),
                password=get_password_hash(admin.password),
            )
        )
