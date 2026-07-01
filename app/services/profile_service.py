from app.models.user import User
from app.schemas.user import UserUpdate
from app.services.user_service import UserService


class ProfileService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_profile(self, current_user: User):
        return current_user

    def update_profile(self, current_user: User, user_update: UserUpdate):
        return self.user_service.update_user(current_user.id, user_update)

    def delete_profile(self, current_user: User):
        return self.user_service.delete_user(current_user.id)
