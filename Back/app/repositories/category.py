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
