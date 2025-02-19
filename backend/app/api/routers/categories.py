from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from backend.app.config.db import connection
from backend.app.db.models.category_model import categories
from backend.app.db.schemas.category_schema import Category, CreateCategory

category_router = APIRouter()


@category_router.get(path='/', tags=['Categories'])
def get_categories() -> Category:
    return connection.execute(categories.select()).fetchall()

@category_router.post(path='/', tags=['Categories'])
def create_category(category:CreateCategory):

     new_category = category.model_dump()

     try:
         #insert
         result = connection.execute(categories.insert().values(new_category))
         connection.commit()

         if result:
             query = connection.execute(categories.select().where(categories.c.id == result.lastrowid)).fetchone()
             print(query)


             if query:
                 content = dict(query._mapping) # Convierto a diccionario de datos

                 return JSONResponse(content=content, status_code=201)

             return JSONResponse(content={"error": "Category not found"})

         else:
            return JSONResponse(content={'message': "'can't insert value'"})
     except SQLAlchemyError as e:
         connection.rollback()
         return JSONResponse(content={"error": str(e)}, status_code=500)



