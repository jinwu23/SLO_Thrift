from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    dependencies=[Depends(auth.get_api_key)],
)

class Store(BaseModel):
    name: str
    address: str
    type: str

@router.get("/", tags=["stores"])
def get_stores():
    """
    Retrieves the catalog of thrift stores in website.
    """
    stores_arr = []
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT stores.id, stores.name, stores.address, stores.type, AVG(reviews.rating) as rating FROM stores JOIN reviews on reviews.store_id = stores.id GROUP BY stores.id"))
        for row in results:
            stores_arr.append(
                {   
                    "id": row.id,
                    "name": row.name,
                    "rating": row.rating,
                    "address": row.address,
                    "type": row.type,
                }
            )
    print("get_stores")
    return stores_arr

@router.get("/{id}")
def get_specific_store(id: int):
    """
    Get a specific thrift store given id
    """
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT stores.id, stores.name, stores.address, stores.type, AVG(reviews.rating) as rating FROM stores JOIN reviews on reviews.store_id = stores.id WHERE stores.id = :id GROUP BY stores.id"), {"id": id})
        row = results.fetchone()
        if row:
            store_stats = {
                "id": row.id,
                "name": row.name,
                "rating": row.rating,
                "address": row.address,
                "type": row.type,
            }
        else:
            store_stats = {}
    return store_stats

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
                (name, address, type)
                VALUES(:name, :address, :type)
                """
            ),
            [{"name": new_store.name, "address": new_store.address, "type": new_store.type}]
        )
    return "OK"

@router.post("/update_name/{store_id}")
def update_name(store_id: int, new_name: str):
    """
    Updates the name of specific store
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE stores
                SET name = :name
                where id = :id
                """
            ),
            [{"name": new_name, "id": store_id}]
        )
    return "OK"

@router.post("/update_address/{store_id}")
def update_address(store_id: int, new_address: str):
    """
    Updates the address of specific store
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE stores
                SET address = :address
                where id = :id
                """
            ),
            [{"address": new_address, "id": store_id}]
        )
    return "OK"

@router.post("/update_type/{store_id}")
def update_type(store_id: int, new_type: str):
    """
    Updates the type of specific store
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE stores
                SET type = :type
                where id = :id
                """
            ),
            [{"type": new_type, "id": store_id}]
        )
    return "OK"