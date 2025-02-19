
from fastapi import FastAPI

from backend.app.api.routers.categories import category_router
from backend.app.api.routers.products import product_router
from backend.app.config.db import engine, meta
from backend.app.db.models.category_model import categories
from backend.app.db.models.product_model import products
from backend.app.db.models.activity_model import activities

app = FastAPI()
app.include_router(product_router, prefix="/products")
app.include_router(category_router, prefix="/categories")

#created tables database
meta.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Hello"}