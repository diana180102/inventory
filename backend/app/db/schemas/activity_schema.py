from datetime import datetime

from pydantic import BaseModel, field_validator


from backend.app.db.schemas.product_schema import Product
from typing import Optional


def type_validator( value):
    if value != "in" and value != "out":
        raise ValueError('type is incorrect')
    return value

def quantity_validator( value):
    if value < 0:
        raise ValueError('Quantity most be greater than 0 ')
    return value


class BaseActivity(BaseModel):
    id: int
    product_id: Product
    type: str
    quantity:int
    Date: datetime


class CreateActivity(BaseModel):
    product_id: int
    type: str
    quantity:int


    class Config:
        from_attributes = True

    _validate_type = field_validator("type")(type_validator)
    _validate_quantity = field_validator("quantity")(quantity_validator)



class UpdateActivity(BaseModel):
    product_id: int | None = None
    type: Optional[str]
    quantity: Optional[int]

    class Config:
        from_attributes = True

    _validate_type = field_validator("type")(type_validator)
    _validate_quantity = field_validator("quantity")(quantity_validator)

