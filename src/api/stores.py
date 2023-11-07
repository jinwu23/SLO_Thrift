from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    dependencies=[Depends(auth.get_api_key)],
)

class Store(BaseModel):
    name: str
    rating: str
    address: str
    type: str

@router.get("/", tags=["stores"])
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
def get_specific_store(store_id: int, id: int):
    """
    A review for a thrift store of reviews for a store.
    """
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE store_id = :store_id AND id = :id"), {"store_id": store_id, "id": id})

        review = results.fetchone()

    return review

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

@router.post("/update_rating/{store_id}")
def update_rating(store_id: int, new_rating: int):
    """
    Updates the rating of specific store
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE stores
                SET rating = :rating
                where id = :id
                """
            ),
            [{"rating": new_rating, "id": store_id}]
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