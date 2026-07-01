from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.schemas.user import UserCreate, UserInLogin
from app.services.user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.user_service = UserService(db)

    def register(self, user: UserCreate):
        hashed_password = hash_password(user.password)

        db_user = self.user_service.create_user(
            user,
            hashed_password,
        )

        token = create_access_token(
            {
                "sub": str(db_user.id),
                "email": db_user.email,
            }
        )

        return {
            "user": db_user,
            "access_token": token,
            "token_type": "bearer",
        }

    def login(self, login_data: UserInLogin):
        user = self.user_service.get_user_by_email(
            login_data.email
        )

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(
            login_data.password,
            user.password,
        ):
            raise InvalidCredentialsError()

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "user": user,
            "access_token": token,
            "token_type": "bearer",
        }