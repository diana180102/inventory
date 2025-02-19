from xmlrpc.client import DateTime

from pydantic import BaseModel, field_validator

from backend.app.db.schemas.product_schema import Product
from typing import Optional


class Activity(BaseModel):
    id:Optional[int]
    product_id: Product
    type: str
    quantity:int
    Date: DateTime

    class Config:
        from_attributes = True


    @field_validator('type')
    def type_validator(cls, value):
        if value != "in" or value != "out":
            raise ValueError('type is incorrect')
        return value

    @field_validator('quantity')
    def quantity_validator(cls, value):
        if value < 0:
            raise ValueError('Quantity most be greater than 0 ')
        return value