from fastapi import APIRouter

from app.schemas.user import UserCreate, UserInLogin

router = APIRouter()

@router.post("/login")
def login(loginDetails:UserInLogin):
    return {"data": loginDetails}

@router.post("/signup")
def signup(signupDetails:UserCreate):
    return {"data": signupDetails}