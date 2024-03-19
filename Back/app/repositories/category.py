from sqlalchemy import BinaryExpression, select
from Back.app.models.category import Category


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def add(self, name, description):
        try:
            category = Category(name, description)
            self.session.add(category)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            categories = self.session.query(Category).all()
            return categories
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Category, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Category)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e

    def update(self, category_id, new_data):
        try:
            category = self.session.query(Category).filter_by(id=category_id).first()
            if category:
                for key, value in new_data.items():
                    setattr(category, key, value)
                self.session.commit()
            else:
                raise ValueError("Category not found.")
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, category_id):
        try:
            category = self.session.query(Category).filter_by(id=category_id).first()
            if category:
                self.session.delete(category)
                self.session.commit()
            else:
                raise ValueError("Category not found.")
        except Exception as e:
            self.session.rollback()
            raise e
