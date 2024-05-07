from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from app.base import Base


class User(Base):
    __tablename__ = "User"

    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String(50), nullable=False, unique=True)
    name = mapped_column(String(20), nullable=False)
    surname = mapped_column(String(50), nullable=False)
    password = mapped_column(String(255), nullable=False)
    type = mapped_column(String, nullable=False)
    profile_picture = mapped_column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "User",
        "polymorphic_on": type,
    }

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}', type='{self.type}'. profile_picture='{self.profile_picture}')"
