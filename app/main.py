from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.database import Base, engine
from app.core.exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenException,
)

# Import models so SQLAlchemy registers them
from app.models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"},
    )


@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists"},
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid email or password"},
    )


@app.exception_handler(InvalidTokenException)
async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException,
):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or expired token"},
    )