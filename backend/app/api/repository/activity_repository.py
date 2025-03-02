from sqlalchemy.exc import SQLAlchemyError


from backend.app.config.db import connection
from backend.app.db.models.activity_model import activities
from sqlalchemy import insert, select, update, delete

from backend.app.db.models.product_model import products


class ActivityRepository:

   @staticmethod
   def get_activities():

       try:
           query = select(
               activities.c.id,
               activities.c.type,
               activities.c.quantity,
               activities.c.Date,
               products.c.id.label("product_id"),
               products.c.name.label("name")
           ).join(products, products.c.id == activities.c.product_id)

           result = connection.execute(query).fetchall()

           activity_list = [
               {
                   "id": row.id,
                   "type": row.type,
                   "quantity":row.quantity,
                   "date": row.Date,
                   "product":{
                       "id": row.product_id,
                       "name":row.name
                   }


               }
               for row in result
           ]

           return activity_list

       except SQLAlchemyError as e:
           raise Exception(f"Database error: {str(e)}")

   @staticmethod
   def get_activity_by_id(id:int):

      try:
           activity = connection.execute(select(activities).where(activities.c.id == id)).fetchone()

           return dict(activity._mapping) if activity else None
      except SQLAlchemyError as e:
          Exception(f"Error database {str(e)}")

   @staticmethod
   def insert_activity(activity):
       try:
           with connection.begin():

               new_activity = connection.execute(
                   insert(activities).values(activity)
               )

               if new_activity.rowcount > 0:

                   query = connection.execute(
                       select(activities).where(
                           activities.c.id == new_activity.lastrowid
                       )
                   ).fetchone()


                   product_id = activity.get("product_id")
                   quantity = activity.get("quantity", 0)
                   activity_type = activity.get("type")

                   if product_id and quantity > 0:
                       if activity_type == "in":
                           # Sumar stock
                           connection.execute(
                               update(products)
                               .where(products.c.id == product_id)
                               .values(stock=products.c.stock + quantity)
                           )
                       elif activity_type == "out":
                           # Restar stock
                           connection.execute(
                               update(products)
                               .where(products.c.id == product_id)
                               .values(stock=products.c.stock - quantity)
                           )

                   return dict(query._mapping) if query else None

       except SQLAlchemyError as e:
           connection.rollback()
           raise Exception(f"Database error: {str(e)}")

   @staticmethod
   def update_activity(activity, id: int):
       try:
           with connection.begin():

               update_activity = connection.execute(
                   update(activities)
                   .where(activities.c.id == id)
                   .values(**activity)
               )

               if update_activity.rowcount == 0:
                   return None


               query = connection.execute(
                   select(activities)
                   .where(activities.c.id == id)
               ).fetchone()


               product_id = query.product_id
               quantity = activity.get("quantity", 0)
               activity_type = activity.get("type")


               if product_id and quantity > 0:
                   if activity_type == "in":
                       connection.execute(
                           update(products)
                           .where(products.c.id == product_id)
                           .values(stock=products.c.stock + quantity)
                       )
                   elif activity_type == "out":
                       connection.execute(
                           update(products)
                           .where(products.c.id == product_id)
                           .values(stock=products.c.stock - quantity)
                       )

               return dict(query._mapping) if query else None

       except SQLAlchemyError as e:
           raise Exception(f"Database error: {str(e)}")

   @staticmethod
   def delete_activity(id:int):

       try:
           with connection.begin():
               delete_activity = connection.execute(delete(activities).where(activities.c.id == id))

               if delete_activity.rowcount > 0:

                   return {"message": "Success deleted product"}
               else:
                   return None
       except SQLAlchemyError as e:
           connection.rollback()
           raise Exception(f'Database error: {str(e)}')
















