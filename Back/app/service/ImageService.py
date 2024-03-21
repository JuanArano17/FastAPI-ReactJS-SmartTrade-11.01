from sqlalchemy.orm import Session
from Back.app.models.image import Image
from repository import Repository


class ImageService:
    def __init__(self, session: Session):
        self.session = session
        self.image_repo = Repository(session, Image)

    def add_image(self, id_product, url):
        try:
            image = self.image_repo.add(id_product=id_product, url=url)
            return image
        except Exception as e:
            raise e

    def list_images(self):
        try:
            return self.image_repo.list()
        except Exception as e:
            raise e

    def get_image(self, image_id):
        try:
            return self.image_repo.get(image_id)
        except Exception as e:
            raise e

    def filter_images(self, *expressions):
        try:
            return self.image_repo.filter(*expressions)
        except Exception as e:
            raise e

    def update_image(self, image_id, new_data):
        try:
            image_instance = self.image_repo.get(image_id)
            if image_instance:
                self.image_repo.update(image_instance, new_data)
                return image_instance
            else:
                raise ValueError("Image not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()

    def delete_image(self, image_id):
        try:
            image_instance = self.image_repo.get(image_id)
            if image_instance:
                self.image_repo.delete(image_instance)
            else:
                raise ValueError("Image not found.")
        except Exception as e:
            raise e
        finally:
            self.session.close()
