from fastapi import APIRouter, HTTPException, Query

from app.api.deps import ImageServiceDep
from app.schemas.products.image import Image, ImageCreate, ImageUpdate

router = APIRouter(prefix="/products/{product_id}/images", tags=["Images"])


@router.get("/", response_model=list[Image])
async def read_images(*, product_id: int, image_service: ImageServiceDep):
    """
    Retrieve images from product.
    """
    return image_service.get_by_id_product(id_product=product_id)


@router.post("/", response_model=Image)
async def create_image(
    *, product_id: int, image: ImageCreate, image_service: ImageServiceDep
):
    """
    Create a new image for the product.
    """
    return image_service.add(id_product=product_id, image=image)


@router.delete("/")
async def delete_images(product_id: int, image_service: ImageServiceDep):
    """
    Delete all image from a product.
    """
    return image_service.delete_by_id_product(product_id)


@router.get("/{image_id}", response_model=Image)
async def read_image(*, product_id: int, image_id: int, image_service: ImageServiceDep):
    """
    Retrieve a specific product image.
    """

    image = image_service.get_by_id(image_id)

    if image is None or image.id_product != product_id:
        raise HTTPException(status_code=404, detail="Image not found")

    return image


@router.put("/{image_id}", response_model=Image)
async def update_image(
    *, product_id=int, image_id: int, image: ImageUpdate, image_service: ImageServiceDep
):
    """
    Update an image.
    """
    existing_image = image_service.get_by_id(image_id)

    if existing_image is None or existing_image.id_product != int(product_id):
        raise HTTPException(status_code=404, detail="Image not found")

    return image_service.update(image_id=image_id, new_data=image)


@router.delete("/{image_id}")
async def delete_image(
    *, product_id=int, image_id: int, image_service: ImageServiceDep
):
    """
    Delete an image.
    """
    existing_image = image_service.get_by_id(image_id)

    if existing_image is None or existing_image.id_product != int(product_id):
        raise HTTPException(status_code=404, detail="Address not found")

    return image_service.delete_by_id(image_id)


image_router = APIRouter(prefix="/images", tags=["Images"])


@image_router.get("/", response_model=dict[int, list[Image]])
async def get_images_for_products(
    *,
    product_ids: list[int] = Query(..., description="List of product IDs"),
    image_service: ImageServiceDep,
):
    """
    Retrieve all images for a list of products.
    """
    images_by_product = {}
    for product_id in product_ids:
        images = image_service.get_by_id_product(id_product=product_id)
        if images:
            images_by_product[product_id] = images
    return images_by_product
