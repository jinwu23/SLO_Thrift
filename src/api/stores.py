from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/store",
    tags=["store"],
    dependencies=[Depends(auth.get_api_key)],
)

class Store(BaseModel):
    name: str
    address: str
    rating: int
    description: str

@router.get("/stores/", tags=["stores"])
def get_stores():
    """
    Retrieves the catalog of thrift stores in website.
    """
    stores_arr = []
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT * FROM stores"))
        for row in results:
            stores_arr.append(
                {
                    "name": row.name,
                    "rating": row.rating,
                    "address": row.address,
                    "type": row.type,
                }
            )
    print("get_stores")
    return stores_arr
