import os
import dotenv
import sqlalchemy
from faker import Faker
import numpy as np
import random

# gets local database_connection_url from .env
def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url())

with engine.begin() as conn:
    conn.execute(sqlalchemy.text(
    """
    create index store_name_idx on stores(name)
    """))
