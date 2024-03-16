from Back.app.models.image import Image


class ImageRepository:
    def __init__(self, session):
        self.session = session

    def add(self, id_product, url):
        image = Image(id_product, url)
        self.session.add(image)
        self.session.commit()
