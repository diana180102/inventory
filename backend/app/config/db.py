import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from pathlib import Path


#"load .env"
env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_path)





SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")


if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Not found url database")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
meta = MetaData()

try:
    connection = engine.connect()
    print("Success connection")
except Exception as e:
    print(f"Error with connection to database: {e}")
