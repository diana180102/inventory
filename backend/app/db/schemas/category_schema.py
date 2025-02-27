from typing import Optional

from pydantic import BaseModel, field_validator


class Category(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        from_attributes = True


class CreateCategory(BaseModel):
    name: str

    @field_validator('name')
    def name_validator(cls, value):
        if len(value) < 6:
            raise ValueError('Name field must have a minimum length of 15 characters')
        if len(value) > 255:
            raise ValueError('Name field must have a maximum length of 255 characters')
        return value

    class Config:
        from_attributes = True



