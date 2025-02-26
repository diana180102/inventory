from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from backend.app.config.db import connection
from backend.app.db.models.product_model import products
from backend.app.db.schemas.product_schema import Product, CreateProduct

product_router = APIRouter()

@product_router.get("/", tags=['Products'])
def get_products() -> Product:
    return connection.execute(products.select()).fetchall()

@product_router.post("/", tags=['Products'], response_model=None)
def create_product(product:CreateProduct) -> JSONResponse:

    # new_product = {
    #     "name": product.name,
    #     "description": product.description,
    #     "stock": product.stock,
    #     "price": product.price,
    #     "category_id": product.category_id
    # }

    new_product = product.model_dump()
    try:
        #insert product
        result = connection.execute(products.insert().values(new_product))
        connection.commit()

        #Get Product created
        query = products.select().where(products.c.id == result.lastrowid)
        product_row = connection.execute(query).fetchone()

        if product_row:
            content = dict(product_row._mapping)
            return JSONResponse(content=content, status_code=201)

        return  JSONResponse(content={"error": "Product not found"})
    except SQLAlchemyError as e:
        connection.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)


