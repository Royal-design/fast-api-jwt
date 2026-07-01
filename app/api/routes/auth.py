from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_bearer_token
from app.core.database import get_db
from app.core.responses import success_response
from app.schemas.user import LogoutRequest, RefreshTokenRequest, UserCreate, UserInLogin
from app.services.auth_service import AuthService


router = APIRouter()

@router.post("/signup")
def signup(signupDetails:UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    result =  auth_service.register(signupDetails)
    return success_response(
        data=result,
        message="User created successfully",
        status_code=201,
    )
   

@router.post("/login")
def login(
    login_details: UserInLogin,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result =  auth_service.login(login_details)
    return success_response(
        data=result,
        message="User logged in successfully",
        status_code=200,
    )


@router.post("/refresh")
def refresh_token(
    refresh_details: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result = auth_service.refresh(refresh_details)
    return success_response(
        data=result,
        message="Token refreshed successfully",
        status_code=200,
    )


@router.post("/logout")
def logout(
    logout_details: LogoutRequest | None = None,
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result = auth_service.logout(
        token,
        logout_details.refresh_token if logout_details else None,
    )
    return success_response(
        data=result,
        message="User logged out successfully",
        status_code=200,
    )
