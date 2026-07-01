from pathlib import Path

from decouple import AutoConfig


BASE_DIR = Path(__file__).resolve().parents[2]
config = AutoConfig(search_path=BASE_DIR)


DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
CLOUDINARY_URL = config("CLOUDINARY_URL", default="")
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY", default="")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", default="")
CLOUDINARY_PROFILE_FOLDER = config("CLOUDINARY_PROFILE_FOLDER", default="fast-api-jwt/profiles")
CLOUDINARY_PRODUCT_FOLDER = config("CLOUDINARY_PRODUCT_FOLDER", default="fast-api-jwt/products")
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    default=30,
    cast=int,
)
REFRESH_TOKEN_EXPIRE_DAYS = config(
    "REFRESH_TOKEN_EXPIRE_DAYS",
    default=7,
    cast=int,
)
