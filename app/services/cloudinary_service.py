import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
)
from app.core.exceptions import ImageUploadError


class CloudinaryService:
    def __init__(self):
        if not (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET):
            raise ImageUploadError("Cloudinary credentials are not configured")

        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )

    def upload_image(self, image: UploadFile, folder: str):
        if not image.content_type or not image.content_type.startswith("image/"):
            raise ImageUploadError("Only image uploads are allowed")

        try:
            result = cloudinary.uploader.upload(
                image.file,
                folder=folder,
                resource_type="image",
            )
        except Exception as exc:
            raise ImageUploadError(f"Could not upload image: {exc}") from exc

        return {
            "image_url": result["secure_url"],
            "image_public_id": result["public_id"],
        }

    def delete_image(self, public_id: str | None):
        if not public_id:
            return

        try:
            cloudinary.uploader.destroy(public_id, resource_type="image")
        except Exception:
            pass
