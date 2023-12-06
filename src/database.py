import os
import dotenv
import sqlalchemy
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

try:
    engine = create_engine(database_connection_url(), pool_pre_ping=True)
except Exception as e:
    print(f"Error connecting to the database: {e}")

metadata_obj = sqlalchemy.MetaData()
stores = sqlalchemy.Table("stores", metadata_obj, autoload_with=engine)
reviews = sqlalchemy.Table("reviews", metadata_obj, autoload_with=engine)
replies = sqlalchemy.Table("replies", metadata_obj, autoload_with=engine)