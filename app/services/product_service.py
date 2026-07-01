from sqlalchemy.orm import Session

from app.core.exceptions import ProductNotFoundError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.cloudinary_service import CloudinaryService


class ProductService:
    def __init__(
        self,
        db: Session,
        cloudinary_service: CloudinaryService | None = None,
    ):
        self.db = db
        self._cloudinary_service = cloudinary_service

    @property
    def cloudinary_service(self) -> CloudinaryService:
        if self._cloudinary_service is None:
            self._cloudinary_service = CloudinaryService()

        return self._cloudinary_service

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ProductNotFoundError("Product not found")

        return product

    def create_product(self, product: ProductCreate):
        db_product = Product(**product.model_dump())

        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)

        return db_product

    def update_product(self, product_id: int, product: ProductUpdate):
        db_product = self.get_product_by_id(product_id)
        updates = product.model_dump(exclude_unset=True)

        for key, value in updates.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)

        return db_product

    def update_product_image(self, product_id: int, image_url: str, image_public_id: str):
        product = self.get_product_by_id(product_id)
        self.cloudinary_service.delete_image(product.image_public_id)

        product.image_url = image_url
        product.image_public_id = image_public_id

        self.db.commit()
        self.db.refresh(product)

        return product

    def delete_product(self, product_id: int):
        product = self.get_product_by_id(product_id)

        self.cloudinary_service.delete_image(product.image_public_id)
        self.db.delete(product)
        self.db.commit()

        return {"message": "Product deleted successfully"}
