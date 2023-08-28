from datetime import datetime
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=3)


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    product_name: str = Field(title="Name", max_length=50)
    description: str = Field(title="Description", max_length=1000)
    price: int = Field(title="Price", gt=0, le=1_000_000)


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: datetime = Field(default=datetime.now())
    status: str = Field(default="created")


class Order(BaseModel):
    id: int
    user_id: int
    date: str
    status: str = Field(default="created")
