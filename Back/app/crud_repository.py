from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar
from pydantic import BaseModel

from app.base import Base

T = TypeVar("T", bound=DeclarativeMeta)
S = TypeVar("S", bound=BaseModel)


class CRUDRepository:
    def __init__(self, *, session: Session, model: T) -> None:
        assert issubclass(model, Base), "Model must be a subclass of Base"
        self._db = session
        self._model = model

    def add(self, entity: T) -> T:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def get_all(self) -> list[T]:
        return self._db.query(self._model).all()

    def get_by_id(self, id) -> T | None:
        return self._db.query(self._model).filter(self._model.id == id).first()  # type: ignore

    def get_where(self, *expressions) -> list[T]:
        return self._db.query(self._model).filter(*expressions).all()

    def update(self, entity: T, new_entity: S, exclude_defaults: bool = True) -> T:
        data = new_entity.model_dump(
            exclude_unset=True, exclude_defaults=exclude_defaults
        )
        self._db.query(self._model).filter(self._model.id == entity.id).update({**data})  # type: ignore
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete_by_id(self, id):
        self._db.query(self._model).filter(self._model.id == id).delete()  # type: ignore
        self._db.commit()
        

    def delete_all(self):
        self._db.query(self._model).delete()
        self._db.commit()
        
    def get_id_list(self):
        items=self._db.query(self._model).all()
        ids=[]
        for item in items:
            ids.append(item.id)
        return ids
