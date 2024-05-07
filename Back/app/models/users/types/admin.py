from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column

from app.models.users.types.user import User


class Admin(User):
    __tablename__ = "Admin"

    id = mapped_column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE", name="fk_admin_user_id"),
        primary_key=True,
        index=True,
    )

    __mapper_args__ = {
        "polymorphic_identity": "Admin",
    }

    def __repr__(self):
        return f"Admin(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}')"
