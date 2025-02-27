from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.exc import SQLAlchemyError

from backend.app.api.services.products_services import ProductService

from backend.app.db.schemas.product_schema import Product, CreateProduct, UpdateProduct

product_router = APIRouter()

@product_router.get(path="/", tags=['Products'], response_model=List[Product])
def get_products() -> Product:
    products_list = ProductService.get_products()
    return [dict(product) for product in products_list]

@product_router.get(path="/{id}", tags=["Products"])
def get_product_by_id(id:int):
    product = ProductService.get_product_by_id(id)

    return product

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
        return  ProductService.create_product(new_product)
    except SQLAlchemyError as e:
       raise HTTPException(status_code=400, detail=str(e))


@product_router.put(path="/{id}", tags=["Products"])
def update_product(id:int, product:UpdateProduct):
    return ProductService.update_product(id, product)

@product_router.delete(path="/{id}", tags=["Products"])
def delete_product(id:int):
    return  ProductService.delete_product(id)