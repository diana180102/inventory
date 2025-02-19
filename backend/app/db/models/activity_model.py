from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, func

from backend.app.config.db import meta, engine
from backend.app.db.models.product_model import products

activities = Table("activities", meta,
                   Column("id", Integer, primary_key=True, autoincrement=True),
                         Column("product_id", Integer, ForeignKey("products.id")),
                         Column("type",String(50), nullable=False),
                         Column("quantity", Integer, nullable=False),
                         Column("Date", DateTime, server_default=func.now())
                   )

