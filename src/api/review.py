from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    dependencies=[Depends(auth.get_api_key)],
)

class Review(BaseModel):
    name: str
    rating: int
    description: str
    
@router.get("/{store_id}")
def get_ratings(store_id: int):
    """
    Retrieve the list of reviews for a store.
    """
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE store_id = :store_id"), {"store_id": store_id})

        reviews = []
        for row in results:
            reviews.append(row)

    return reviews

@router.get("/{store_id}/{id}")
def get_specific_rating(store_id: int, id: int):
    """
    A review for a thrift store of reviews for a store.
    """
    with db.engine.begin() as connection:
        results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE store_id = :store_id AND id = :id"), {"store_id": store_id, "id": id})

        review = results.fetchone()

    return review
             
@router.post("/create_review")
def create_review(store_id: int, new_review: Review):
    """
    Creates new thrift review in website.
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO reviews
                (account_name, rating, description, store_id)
                VALUES(:account_name, :rating, :description, :store_id)
                """
            ),
            [{"account_name": new_review.name, "rating": new_review.rating, "description": new_review.description, "store_id": store_id}]
        )
    return "OK"
