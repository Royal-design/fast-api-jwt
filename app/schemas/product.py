from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int = 0
    image_url: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
    image_url: str | None = None


class ProductOutput(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    quantity: int
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
