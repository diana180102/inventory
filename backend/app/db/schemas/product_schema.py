import decimal

from pydantic import BaseModel, field_validator
from typing_extensions import Optional

from backend.app.db.schemas.category_schema import Category


class Product(BaseModel):

    id: Optional[int]
    name:str
    description:str
    stock:int
    price:decimal.Decimal
    category_id:Category




class CreateProduct(BaseModel):
    name: str
    description: str
    stock: int
    price: decimal.Decimal
    category_id: int

    @field_validator('name')
    def validator_name(cls, value):
        if len(value) < 15:
            raise ValueError('Name field must have a minimum length of 15 characters')
        return value

    @field_validator('description')
    def description_validator(cls, value):
        if len(value) < 15:
            raise ValueError('Description field must have a minimum length of 15 characters')
        if len(value) > 255:
            raise ValueError('Description field must have a maximum length of 255 characters')
        return value

    @field_validator('stock')
    def quantity_validator(cls, value):
        if value < 0:
            raise ValueError('Stock most be greater than 0 ')
        return value

    @field_validator('price')
    def quantity_validator(cls, value):
        if value < 0:
            raise ValueError('price most be greater than 0 ')
        return value

    class Config:
        from_attributes = True  # Para trabajar con SQLAlchemy