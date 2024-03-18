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
