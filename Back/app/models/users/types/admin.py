from sqlalchemy import Column, ForeignKey, Integer

from app.models.users.types.user import User


class Admin(User):
    __tablename__ = "Admin"

    id = Column(
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
