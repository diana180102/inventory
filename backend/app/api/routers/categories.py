
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from backend.app.config.db import connection
from backend.app.db.models.category_model import categories
from backend.app.db.schemas.category_schema import Category, CreateCategory

category_router = APIRouter()


@category_router.get(path='/', tags=['Categories'])
def get_categories() -> Category:
    query = connection.execute(categories.select()).fetchall()
    content = [dict(row._mapping) for row in query]
    return JSONResponse(content= content, status_code=200)



@category_router.get(path='/{id}', tags=['Categories'])
def get_categories_by_id(id:int) -> Category:
    query = connection.execute(categories.select().where(id == categories.c.id)).fetchone()

    if query:
        content = dict(query._mapping)
        return JSONResponse(content=content, status_code=200)
    else:
        return JSONResponse(content={"error": "Category not found"})



@category_router.post(path='/', tags=['Categories'])
def create_category(category:CreateCategory):

     new_category = category.model_dump()

     try:
         #insert
         result = connection.execute(categories.insert().values(new_category))
         connection.commit()

         if result:
             query = connection.execute(categories.select().where(categories.c.id == result.lastrowid)).fetchone()



             if query:
                 content = dict(query._mapping) # Convierto a diccionario de datos

                 return JSONResponse(content=content, status_code=201)

             return JSONResponse(content={"error": "Category not found"})

         else:
            return JSONResponse(content={'message': "'can't insert value'"})
     except SQLAlchemyError as e:
         connection.rollback()
         return JSONResponse(content={"error": str(e)}, status_code=500)


@category_router.put(path='/{id}', tags=['Categories'])
def update_category(category: CreateCategory, id: int):
    category_data = category.model_dump(exclude_unset=True)  # Solo incluye campos enviados

    try:

        update_query = connection.execute(
            categories.update()
            .where(categories.c.id == id)
            .values(**category_data)
        )
        connection.commit()


        if update_query.rowcount > 0:

            query = connection.execute(categories.select().where(categories.c.id == id)).fetchone()

            if query:
                content = dict(query._mapping)
                return JSONResponse(content=content, status_code=200)
            else:
                return JSONResponse(content={"error": "Category not found"}, status_code=404)

        return JSONResponse(content={"error": "Unable to update"}, status_code=404)

    except SQLAlchemyError as e:
        connection.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)


@category_router.delete(path='/{id}', tags=['Categories'])
def delete_category(id:int):
    query = connection.execute(categories.delete().where(categories.c.id == id))
    connection.commit() #confirmación de transacción

    if query.rowcount > 0:
        return JSONResponse(content={"message": "Category deleted successfully"}, status_code=200)
    else:
        return JSONResponse(content={"error": "Category not found"}, status_code=404)





