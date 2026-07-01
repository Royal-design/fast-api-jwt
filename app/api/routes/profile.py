from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import CLOUDINARY_PROFILE_FOLDER
from app.core.database import get_db
from app.core.responses import success_response
from app.models.user import User
from app.schemas.user import UserOutput, UserUpdate
from app.services.cloudinary_service import CloudinaryService
from app.services.profile_service import ProfileService
from app.services.user_service import UserService


router = APIRouter()


def get_profile_service(db: Session = Depends(get_db)):
    return ProfileService(UserService(db))


def serialize_profile(user: User) -> UserOutput:
    return UserOutput.model_validate(user)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
):
    profile = profile_service.get_profile(current_user)
    return success_response(
        data=serialize_profile(profile),
        message="Profile fetched successfully",
    )


@router.patch("/me")
def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
):
    profile = profile_service.update_profile(current_user, user_update)
    return success_response(
        data=serialize_profile(profile),
        message="Profile updated successfully",
    )


@router.patch("/me/image")
def update_my_profile_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
):
    upload = CloudinaryService().upload_image(image, CLOUDINARY_PROFILE_FOLDER)
    profile = profile_service.update_profile_image(
        current_user,
        upload["image_url"],
        upload["image_public_id"],
    )
    return success_response(
        data=serialize_profile(profile),
        message="Profile image updated successfully",
    )


@router.delete("/me")
def delete_my_profile(
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
):
    result = profile_service.delete_profile(current_user)
    return success_response(data=result, message="Profile deleted successfully")
