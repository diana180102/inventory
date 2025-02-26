from backend.app.config.db import connection
from backend.app.db.models.activity_model import activities
from sqlalchemy import insert, select


class ActivityRepository:

    @staticmethod
    def insert_activity(activity):
        with connection.begin():
            result = connection.execute(insert(activities).values(activity))
            return result.lastrowid


    @staticmethod
    def get_activity_by_id(id:int):
        with connection.begin():
           query = connection.execute(select(activities).where(activities.c.id == id))
        return connection.execute(query).fetchone()
