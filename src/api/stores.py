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
    rating: int
    address: str
    type: str

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

@router.post("/create_store")
def create_store(new_store: Store):
    """
    Creates new thrift stores in website.
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO stores
                (name, rating, address, type)
                VALUES(:name, :rating, :address, :type)
                """
            ),
            [{"name": new_store.name, "rating": new_store.rating, "address": new_store.address, "type": new_store.type}]
        )
    return "OK"