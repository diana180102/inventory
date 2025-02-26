
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse


from backend.app.config.db import connection
from backend.app.db.models.activity_model import activities
from backend.app.db.schemas.activity_schema import CreateActivity
from backend.app.db.schemas.category_schema import CreateCategory

activity_router = APIRouter()

@activity_router.get(path='/', tags=['activity'])
def get_activities():
    query = connection.execute(activities.select()).fetchall()
    content = [dict(row._mapping) for row in query]
    return JSONResponse(content= content, status_code=200)

@activity_router.get(path='/{id}', tags=['activity'])
def get_activity_by_id(id:int):
    query = connection.execute(activities.select().where(id == activities.c.id)).fetchone()

    if query:
        content = dict(query._mapping)
        return JSONResponse(content= content, status_code=200)
    else:
        return JSONResponse(content={"error": "Activity not found"})


@activity_router.post(path='/', tags=['activity'])
def create_activity(activity:CreateActivity):

    new_activity = activity.model_dump()  #convierte a diccionario de datos

    try:
        result = connection.execute(activities.insert().values(new_activity))
        connection.commit()

        if result:
            query = connection.execute(activities.select().where(activities.c.id == result.lastrowid)).fetchone()

            if query:
                content = dict(query._mapping)

                return JSONResponse(content, status_code=201)
            return JSONResponse(content={"error": "Activity not found"})

        else:
            return JSONResponse(content={'message': "'can't insert value'"})
    except SQLAlchemyError as e:
        connection.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)

@activity_router.put(path='/{id}', tags=['activity'])
def update_activity(activity:CreateActivity, id:int):

    activity_data = activity.model_dump(exclude_unset=True)

    try:
        update_query = connection.execute(
            activities.update()
            .where(activities.c.id == id)
            .values(**activity_data))

        connection.commit()

        if update_query.rowcount > 0 :

            query = connection.execute(activities.select().where(activities.c.id == id)).fetchone()

            if query:
                content = dict(query._mapping)
                return JSONResponse(content=content, status_code=200)
            else:
                return JSONResponse(content={"error": "Activity not found"}, status_code=404)

        return JSONResponse(content={"error": "Unable to update"}, status_code=404)

    except SQLAlchemyError as e:
        connection.rollback()
        return JSONResponse(content={"error": str(e) }, status_code=500)


@activity_router.delete(path='/{id}', tags=['activity'])
def delete_activity(id:int):

    query = connection.execute(activities.delete().where(activities.c.id == id))
    connection.commit()

    if query.rowcount > 0:
        return JSONResponse(content={"message": "Activity deleted successfully"}, status_code=200)
    else:
        return JSONResponse(content={"error": "Activity not found"}, status_code=404)




