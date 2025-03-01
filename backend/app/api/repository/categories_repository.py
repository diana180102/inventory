
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError


from backend.app.config.db import connection
from backend.app.db.models.category_model import categories



class CategoriesRepository:

    @staticmethod
    def get_categories():
        try:

            with connection.begin():
                categories_list = connection.execute(select(categories)).fetchall()

                return [dict(category._mapping) for category in categories_list]
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_category_by_id(id:int):
        try:
            with connection.begin():
                category = connection.execute(select(categories).where(categories.c.id == id)).fetchone()

                if not category:
                    return {"error:" "not found category in database"}

                return dict(category._mapping)
        except SQLAlchemyError as e:
            raise Exception(f"Database error:{str(e)}")

    @staticmethod
    def insert_category(category):

        try:
            with connection.begin():
                category_new = connection.execute(insert(categories).values(category))

                if category_new.rowcount > 0:
                    query = connection.execute(
                        select(categories)
                        .where(categories.c.id == category_new.lastrowid)).fetchone()
                return  dict(query._mapping) if query else None

        except SQLAlchemyError as e:
            connection.rollback()
            raise Exception(f"error in database {str(e)}")

    @staticmethod
    def update_category(category, id: int):


        try:
            with (connection.begin()):
                update_category = connection.execute(
                    update(categories)
                    .where(categories.c.id == id)
                    .values(**category))

                if update_category.rowcount == 0:
                    return None

                query = connection.execute(
                    select(categories)
                    .where(categories.c.id == id)
                ).fetchone()

                return dict(query._mapping) if query else None

        except SQLAlchemyError as e:
            connection.rollback()
            raise Exception(f'Database error: {str(e)}')

    @staticmethod
    def delete_category(id:int):
         try:
             with connection.begin():
                 delete_category = connection.execute(delete(categories).where(categories.c.id == id))

                 if delete_category.rowcount > 0:
                     return {"message": "Success deleted category"}
                 else:
                     return None
         except SQLAlchemyError as e:
             connection.rollback()
             raise Exception(f'Database error: {str(e)}')





