
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float
from backend.app.config.db import meta, engine
from backend.app.db.models.category_model import categories

products = Table("products", meta,
                 Column("id", Integer, primary_key=True, autoincrement=True),
                       Column("name", String(255), nullable=False),
                       Column("description", String(255), nullable=False),
                       Column("stock", Integer, nullable=False),
                       Column("price", Float, nullable=False),
                       Column("category_id", Integer, ForeignKey('categories.id'))
                 )

