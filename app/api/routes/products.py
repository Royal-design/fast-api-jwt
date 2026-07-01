from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import CLOUDINARY_PRODUCT_FOLDER
from app.core.database import get_db
from app.core.responses import success_response
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOutput, ProductUpdate
from app.services.cloudinary_service import CloudinaryService
from app.services.product_service import ProductService


router = APIRouter(dependencies=[Depends(get_current_user)])


def serialize_product(product: Product) -> ProductOutput:
    return ProductOutput.model_validate(product)


def filled_fields(**fields):
    return {
        key: value
        for key, value in fields.items()
        if value is not None and value != ""
    }


@router.get("")
def get_products(db: Session = Depends(get_db)):
    products = ProductService(db).get_all_products()
    return success_response(
        data=[serialize_product(product) for product in products],
        message="Products fetched successfully",
    )


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService(db).get_product_by_id(product_id)
    return success_response(
        data=serialize_product(product),
        message="Product fetched successfully",
    )


@router.post("")
async def create_product(
    name: str = Form(...),
    description: str | None = Form(None),
    price: float = Form(...),
    quantity: int = Form(0),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    product = ProductCreate(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    product_service = ProductService(db)
    new_product = product_service.create_product(product)

    if image:
        upload = CloudinaryService().upload_image(image, CLOUDINARY_PRODUCT_FOLDER)
        new_product = product_service.update_product_image(
            new_product.id,
            upload["image_url"],
            upload["image_public_id"],
        )

    return success_response(
        data=serialize_product(new_product),
        message="Product created successfully",
        status_code=201,
    )


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    price: float | None = Form(None),
    quantity: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    product = ProductUpdate.model_validate(
        filled_fields(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )
    )
    product_service = ProductService(db)
    updated_product = product_service.update_product(product_id, product)

    if image:
        upload = CloudinaryService().upload_image(image, CLOUDINARY_PRODUCT_FOLDER)
        updated_product = product_service.update_product_image(
            product_id,
            upload["image_url"],
            upload["image_public_id"],
        )

    return success_response(
        data=serialize_product(updated_product),
        message="Product updated successfully",
    )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    result = ProductService(db).delete_product(product_id)
    return success_response(data=result, message="Product deleted successfully")
