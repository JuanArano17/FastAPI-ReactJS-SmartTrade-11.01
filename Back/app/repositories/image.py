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
