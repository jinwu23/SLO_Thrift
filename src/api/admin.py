from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from sqlalchemy import text

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)
class Description(BaseModel):
    description: str

@router.delete("/store/{store_id}")
def delete_store(store_id: int):
    """
    a call to delete store will delete the selected store
    """
    with db.engine.begin() as connection: 

        # # performance testing query
        # performance_results = connection.execute(text(
        #     "EXPLAIN ANALYZE DELETE FROM stores where id=:id"
        # ), {"id":store_id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        # check if store exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT count(*)
                FROM stores
                WHERE id = :store_id
                """
            ),
            {"store_id": store_id}
        )
        if result.scalar_one() == 0:
            return "Store does not exist"
        
        connection.execute(sqlalchemy.text("DELETE FROM stores where id=:id"),{"id":store_id})
    return "OK"

@router.delete("/reset/{store_id}")
def reset(store_id: int):
    """
    a call to reset reviews will delete all reviews under a specific store
    """
    with db.engine.begin() as connection:

        # # performance testing query
        # performance_results = connection.execute(text(
        #     "EXPLAIN ANALYZE DELETE FROM reviews WHERE store_id=:id"
        # ), {"id":store_id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        # check if store exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT count(*)
                FROM stores
                WHERE id = :store_id
                """
            ),
            {"store_id": store_id}
        )
        if result.scalar_one() == 0:
            return "Store does not exist"

        connection.execute(sqlalchemy.text("DELETE FROM reviews WHERE store_id=:id"), {"id": store_id})

    return "OK"

@router.delete("/review/{review_id}")
def delete_review(review_id: int): 
    """
    a call to delete a specific review
    """
    print(review_id)
    with db.engine.begin() as connection: 

        # # performance testing query
        # performance_results = connection.execute(text(
        #     "EXPLAIN ANALYZE DELETE FROM reviews WHERE id=:rev_id"
        # ), {"rev_id": review_id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        # check if review exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT count(*)
                FROM reviews
                WHERE id = :review_id
                """
            ),
            {"review_id": review_id}
        )
        if result.scalar_one() == 0:
            return "Review does not exist"

        connection.execute(sqlalchemy.text("DELETE FROM reviews WHERE id=:rev_id"), {"rev_id": review_id})
    return "OK"