from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column

from app.base import Base


class Country(Base):
    __tablename__ = "Country"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)

    def __repr__(self):
        return f"Country(id={self.id}, name='{self.name}'"
