from itertools import product

from backend.app.db.schemas.activity_schema import CreateActivity


class ActivityService:

    @staticmethod
    def create_activity(activity: CreateActivity):

        new_activity = activity.model_dump()

