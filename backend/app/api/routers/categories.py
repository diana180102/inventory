
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from backend.app.api.services.categories_service import CategoriesService
from backend.app.config.db import connection
from backend.app.db.models.category_model import categories
from backend.app.db.schemas.category_schema import Category, CreateCategory

category_router = APIRouter()


@category_router.get(path='/', tags=['Categories'])
def get_categories() -> Category:
     content = CategoriesService.get_categories()
     return JSONResponse(content, status_code=200)



@category_router.get(path='/{id}', tags=['Categories'])
def get_categories_by_id(id:int) -> Category:
   content = CategoriesService.get_category_by_id(id)
   return JSONResponse(content=content, status_code=200)




@category_router.post(path='/', tags=['Categories'])
def create_category(category:CreateCategory):

     new_category = category.model_dump()

     content = CategoriesService.create_category(new_category)
     return  JSONResponse(content, status_code=201)


@category_router.put(path='/{id}', tags=['Categories'])
def update_category(category: CreateCategory, id: int):
    category_data = category.model_dump(exclude_unset=True)  # Solo incluye campos enviados

    content = CategoriesService.update_category(category_data, id)
    return JSONResponse(content, status_code=200)



@category_router.delete(path='/{id}', tags=['Categories'])
def delete_category(id:int):
    content = CategoriesService.delete_category(id)
    return JSONResponse(content, status_code=200)





