from sqlalchemy import Column, Integer, String
from app.base import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False, unique=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    type = Column(String, nullable=False)
    profile_picture = Column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "User",
        "polymorphic_on": type,
    }

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', password='{self.password}', type='{self.type}'. profile_picture='{self.profile_picture}')"
