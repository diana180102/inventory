from sqlalchemy.exc import SQLAlchemyError


from backend.app.config.db import connection
from backend.app.db.models.category_model import categories
from backend.app.db.models.product_model import products
from sqlalchemy import select, insert, update, delete



class ProductRepository:

    @staticmethod
    def get_products():
        query = select(
            products.c.id,
            products.c.name.label("product_name"),
            products.c.description,
            products.c.stock,
            products.c.price,
            categories.c.id.label("category_id"),
            categories.c.name.label("category_name")
        ).join(categories, products.c.category_id == categories.c.id)

        result = connection.execute(query).fetchall()

        products_list = [
            {
                "id": row.id,
                "name": row.product_name,
                "description": row.description,
                "stock": row.stock,
                "price": row.price,
                "category": {
                    "id": row.category_id,
                    "name": row.category_name
                }
            }
            for row in result
        ]

        return products_list

    @staticmethod
    def get_product_by_id(id:int):
        query = select(
            products.c.id,
            products.c.name.label("product_name"),
            products.c.description,
            products.c.stock,
            products.c.price,
            categories.c.id.label("category_id"),
            categories.c.name.label("category_name")
        ).join(categories, products.c.category_id == categories.c.id).where(products.c.id == id)

        result = connection.execute(query).fetchone()

        if result is None:
            return None

        product =  {
                "id": result.id,
                "name": result.product_name,
                "description": result.description,
                "stock": result.stock,
                "price": result.price,
                "category": {
                    "id": result.category_id,
                    "name": result.category_name
                }
            }

        return product

    @staticmethod
    def insert_product(product):
        try:
            with connection.begin():
                result = connection.execute(insert(products).values(product))

                if result.rowcount > 0:
                    query = connection.execute(
                        products.select()
                        .where(products.c.id == result.lastrowid)
                    ).fetchone()


                    return dict(query._mapping)  if query else None

        except SQLAlchemyError as e:
            connection.rollback()
            raise  Exception(f'Database error: {str(e)}')

    @staticmethod
    def update_product(id:int, product):


            product_data = product.model_dump(exclude_unset=True)

            try:
                with (connection.begin()):
                    result = connection.execute(
                        update(products)
                        .where(products.c.id == id)
                        .values(**product_data))

                    if result.rowcount == 0:
                        return None

                    query = connection.execute(
                        products.select()
                        .where(products.c.id == id)
                    ).fetchone()
                    return dict(query._mapping) if query else None

            except SQLAlchemyError as e:
                connection.rollback()
                raise Exception(f'Database error: {str(e)}')

    @staticmethod
    def delete_product(id:int):
        try:
            with connection.begin():
                delete_product = connection.execute(delete(products).where(products.c.id == id))

                if delete_product.rowcount > 0:
                    return {"message": "Success deleted product"}
                else:
                    return None
        except SQLAlchemyError as e:
            connection.rollback()
            raise  Exception(f'Database error: {str(e)}')

