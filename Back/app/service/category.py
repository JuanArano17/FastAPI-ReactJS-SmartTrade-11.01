from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.crud_repository import CRUDRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Category)
        self._model = Category

    def get_by_name(self, name: str) -> Category | None:
        return self._db.query(self._model).filter(self._model.name == name).first()

class CategoryService:
    def __init__(self, session: Session):
        self.session = session
        self.category_repo = CategoryRepository(session=session)

    def add(self, category: CategoryCreate) -> Category:
        if self.category_repo.get_by_name(category.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {category.name} already exists.",
            )

        return self.category_repo.add(Category(**category.model_dump()))

    def get_all(self) -> list[Category]:
        return self.category_repo.get_all()

    def get_by_id(self, id: int) -> Category:
        if category := self.category_repo.get_by_id(id):
            return category

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} not found.",
        )

    def update(self, category_id, new_data: CategoryUpdate) -> Category:
        category = self.get_by_id(category_id)
        if new_data.name and self.category_repo.get_by_name(new_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {new_data.name} already exists.",
            )
        return self.category_repo.update(category, new_data)

    def delete_by_id(self, id):
        self.get_by_id(id)
        self.category_repo.delete_by_id(id)

    def delete_all(self):
        self.category_repo.delete_all()
