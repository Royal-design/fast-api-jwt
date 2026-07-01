from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import CLOUDINARY_PRODUCT_FOLDER
from app.core.database import get_db
from app.core.responses import success_response
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.cloudinary_service import CloudinaryService
from app.services.product_service import ProductService


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("")
def get_products(db: Session = Depends(get_db)):
    products = ProductService(db).get_all_products()
    return success_response(data=products, message="Products fetched successfully")


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService(db).get_product_by_id(product_id)
    return success_response(data=product, message="Product fetched successfully")


@router.post("")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    new_product = ProductService(db).create_product(product)
    return success_response(
        data=new_product,
        message="Product created successfully",
        status_code=201,
    )


@router.patch("/{product_id}")
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    updated_product = ProductService(db).update_product(product_id, product)
    return success_response(
        data=updated_product,
        message="Product updated successfully",
    )


@router.patch("/{product_id}/image")
def update_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    upload = CloudinaryService().upload_image(image, CLOUDINARY_PRODUCT_FOLDER)
    product = ProductService(db).update_product_image(
        product_id,
        upload["image_url"],
        upload["image_public_id"],
    )
    return success_response(data=product, message="Product image updated successfully")


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    result = ProductService(db).delete_product(product_id)
    return success_response(data=result, message="Product deleted successfully")
