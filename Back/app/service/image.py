from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.image import ImageCreate, ImageUpdate
from app.models.image import Image
from app.crud_repository import CRUDRepository
from app.service.product import ProductService

class ImageRepository(CRUDRepository):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Image)
        self._model = Image

    def get_by_id_product(self, id_product) -> list[Image]:
        return (
            self._db.query(self._model).filter(self._model.id_product == id_product).all()
        )
    
    def delete_by_id_product(self, id_product):
        self._db.query(self._model).filter(self._model.id_product == id_product).delete()  # type: ignore
        self._db.commit()



class ImageService:
    def __init__(self, session: Session, product_service: ProductService):
        self.session = session
        self.image_repo = ImageRepository(session=session)
        self.product_service = product_service

    def add(self, id_product: int, image: ImageCreate) -> Image:
        self.product_service.get_by_id(id_product)
        image_obj = Image(**image.model_dump(), id_product=id_product)
        image_obj = self.image_repo.add(image_obj)
        return image_obj

    def get_by_id(self, image_id) -> Image:
        if image := self.image_repo.get_by_id(image_id):
            return image

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found.",
        )

    def get_all(self) -> list[Image]:
        return self.image_repo.get_all()

    def update(self, image_id, new_data: ImageUpdate) -> Image:
        image = self.get_by_id(image_id)
        return self.image_repo.update(image, new_data)

    def delete_by_id(self, image_id):
        self.get_by_id(image_id)
        self.image_repo.delete_by_id(image_id)

    def delete_all(self):
        self.image_repo.delete_all()

    def get_by_id_product(self, id_product)-> list[Image]:
        return self.image_repo.get_by_id_product(id_product=id_product)
    
    def delete_by_id_product(self, id_product)-> list[Image]:
        return self.image_repo.delete_by_id_product(id_product=id_product)
    
    