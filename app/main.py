from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import include_api_routes
from app.core.config import CORS_ALLOWED_ORIGINS
from app.core.exceptions import (
    EmailAlreadyExistsError,
    ImageUploadError,
    InvalidCredentialsError,
    InvalidTokenException,
    ProductNotFoundError,
    UserNotFoundError,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in CORS_ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_api_routes(app)


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidTokenException)
async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException,
):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


@app.exception_handler(ImageUploadError)
async def image_upload_error_handler(
    request: Request,
    exc: ImageUploadError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
