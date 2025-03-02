
from fastapi import APIRouter

from fastapi.responses import JSONResponse, ORJSONResponse

from backend.app.api.services.activity_service import ActivityService

from backend.app.db.schemas.activity_schema import CreateActivity, UpdateActivity

activity_router = APIRouter()

@activity_router.get(path='/', tags=['Activities'])
def get_activities():
    activities_list = ActivityService.get_activities()
    if activities_list:
        content = [dict(row) for row in activities_list]
        return ORJSONResponse(content, status_code=200)


@activity_router.get(path='/{id}', tags=['Activities'])
def get_activity_by_id(id:int):

    content = ActivityService.get_activity_by(id)
    return ORJSONResponse(content, status_code=200)



@activity_router.post(path='/', tags=['Activities'])
def create_activity(activity:CreateActivity):

    new_activity = activity.model_dump()  #convierte a diccionario de datos

    content = ActivityService.create_activity(new_activity)

    return ORJSONResponse(content, status_code=201)

@activity_router.put(path='/{id}', tags=['Activities'])
def update_activity(activity:UpdateActivity, id:int):

    activity_data = activity.model_dump(exclude_unset=True)

    content = ActivityService.update_activity(activity_data, id)
    return ORJSONResponse(content, status_code=200)


@activity_router.delete(path='/{id}', tags=['Activities'])
def delete_activity(id:int):

    content = ActivityService.delete_activity(id)
    return JSONResponse(content, status_code=200)




