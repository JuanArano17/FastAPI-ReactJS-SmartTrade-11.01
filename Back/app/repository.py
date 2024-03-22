from sqlalchemy import select
from sqlalchemy.orm import Session


class Repository:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def add(self, **kwargs):
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            return self.session.query(self.model).all()
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.query(self.model).get(pk)
        except Exception as e:
            raise e

    def filter(self, *expressions):
        try:
            query = select(self.model)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.execute(query))
        except Exception as e:
            raise e

    def update(self, instance, new_data):
        try:
            for key, value in new_data.items():
                setattr(instance, key, value)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, instance):
        try:
            self.session.delete(instance)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
