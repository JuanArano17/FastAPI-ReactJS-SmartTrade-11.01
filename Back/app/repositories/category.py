from Back.app.models.category import Category


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def add(self, name, description):
        category = Category(name, description)
        self.session.add(category)
        self.session.commit()
