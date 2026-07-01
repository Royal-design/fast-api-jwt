from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.responses import success_response
from app.models.user import User
from app.schemas.user import UserOutput, UserUpdate, UsersResponse
from app.services.user_service import UserService


router = APIRouter(dependencies=[Depends(get_current_user)])


def serialize_user(user: User) -> UserOutput:
    return UserOutput.model_validate(user)


@router.get("", response_model=UsersResponse)
def get_users(db: Session = Depends(get_db)):
    users = UserService(db).get_all_users()

    return success_response(
        data=[serialize_user(user) for user in users],
        message="Users fetched successfully"
    )


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService(db).get_user_by_id(user_id)
    return success_response(
        data=serialize_user(user),
        message="User fetched successfully",
    )


@router.patch("/{user_id}")
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    user = UserService(db).update_user(user_id, user_update)
    return success_response(data=user, message="User updated successfully")


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    result = UserService(db).delete_user(user_id)
    return success_response(data=result, message="User deleted successfully")
