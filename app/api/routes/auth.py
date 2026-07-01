from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import success_response
from app.schemas.user import UserCreate, UserInLogin
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
