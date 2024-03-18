from sqlalchemy import BinaryExpression, select
from Back.app.models.image import Image


class ImageRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_product, url):
        try:
            image = Image(id_product, url)
            self.session.add(image)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def list(self):
        try:
            images = self.session.query(Image).all()
            return images
        except Exception as e:
            raise e

    def get(self, pk):
        try:
            return self.session.get(Image, pk)
        except Exception as e:
            raise e

    def filter(
        self,
        *expressions: BinaryExpression,
    ):
        try:
            query = select(Image)
            if expressions:
                query = query.where(*expressions)
            return list(self.session.scalars(query))
        except Exception as e:
            raise e
