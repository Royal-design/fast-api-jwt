from app.models.user import User
from app.schemas.user import UserUpdate
from app.services.cloudinary_service import CloudinaryService
from app.services.user_service import UserService


class ProfileService:
    def __init__(
        self,
        user_service: UserService,
        cloudinary_service: CloudinaryService | None = None,
    ):
        self.user_service = user_service
        self._cloudinary_service = cloudinary_service

    @property
    def cloudinary_service(self) -> CloudinaryService:
        if self._cloudinary_service is None:
            self._cloudinary_service = CloudinaryService()

        return self._cloudinary_service

    def get_profile(self, current_user: User):
        return current_user

    def update_profile(self, current_user: User, user_update: UserUpdate):
        return self.user_service.update_user(current_user.id, user_update)

    def update_profile_image(self, current_user: User, image_url: str, image_public_id: str):
        self.cloudinary_service.delete_image(current_user.image_public_id)
        current_user.image_url = image_url
        current_user.image_public_id = image_public_id

        self.user_service.db.commit()
        self.user_service.db.refresh(current_user)

        return current_user

    def delete_profile(self, current_user: User):
        self.cloudinary_service.delete_image(current_user.image_public_id)
        return self.user_service.delete_user(current_user.id)
