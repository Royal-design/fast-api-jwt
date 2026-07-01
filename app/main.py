from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.router import api_router
from app.models.user import User

app = FastAPI()
app.include_router(api_router)

Base.metadata.create_all(bind=engine)