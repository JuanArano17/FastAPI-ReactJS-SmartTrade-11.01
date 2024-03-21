from Back.app.models.category import Category
from repository import Repository
from sqlalchemy.orm import Session


class CategoryService:
    def __init__(self, session: Session):
        self.session = session
        self.category_repo = Repository(session, Category)

    def add_category(self, name, description):
        try:
            category = self.category_repo.add(name=name, description=description)
            return category
        except Exception as e:
            raise e

    def list_categories(self):
        try:
            return self.category_repo.list()
        except Exception as e:
            raise e

    def get_category(self, category_id):
        try:
            return self.category_repo.get(category_id)
        except Exception as e:
            raise e

    def filter_categories(self, *expressions):
        try:
            return self.category_repo.filter(*expressions)
        except Exception as e:
            raise e

    def update_category(self, category_id, new_data):
        try:
            category_instance = self.category_repo.get(category_id)
            if category_instance:
                self.category_repo.update(category_instance, new_data)
                return category_instance
            else:
                raise ValueError("Category not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_category(self, category_id):
        try:
            category_instance = self.category_repo.get(category_id)
            if category_instance:
                self.category_repo.delete(category_instance)
            else:
                raise ValueError("Category not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
