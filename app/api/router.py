from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.profile import router as profile_router
from app.api.routes.users import router as users_router

api_router = APIRouter()


def include_api_routes(app: APIRouter):
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
    app.include_router(profile_router, prefix="/api/v1/profile", tags=["profile"])


include_api_routes(api_router)
