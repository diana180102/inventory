from fastapi import HTTPException

from backend.app.api.repository.activity_repository import ActivityRepository



class ActivityService:

   @staticmethod
   def get_activities():
       try:
            activities_list = ActivityRepository.get_activities()
            return activities_list if activities_list else []
       except Exception as e:
           raise  Exception(f"Error fetching activities: {str(e)}")

   @staticmethod
   def get_activity_by(id:int):

       activity = ActivityRepository.get_activity_by_id(id)
       if not activity:
           raise  HTTPException(status_code=404, detail="Not found activity")
       return  activity

   @staticmethod
   def create_activity(activity):

       activity_new = ActivityRepository.insert_activity(activity)
       if not activity_new:
           return HTTPException(status_code=404, detail="Can´t insert activity")

       return activity_new

   @staticmethod
   def update_activity(activity, id:int):

       update_data = ActivityRepository.update_activity(activity, id)
       if not update_data:
           raise HTTPException(status_code=404, detail="can't update activity")
       return update_data

   @staticmethod
   def delete_activity(id:int):

       delete_activity = ActivityRepository.delete_activity(id)

       if not delete_activity:
           raise HTTPException(status_code=404, detail="can´t delete activity")

       return delete_activity




