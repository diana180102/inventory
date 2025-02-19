from sqlalchemy import Table, Column, Integer, String

from backend.app.config.db import meta, engine

categories = Table("categories", meta,
                  Column("id", Integer, primary_key=True, autoincrement=True),
                        Column("name", String(100), nullable=False)
                  )


