from enum import Enum
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

class Reply(BaseModel):
    name: str
    description: str

MAXRATING = 5
MINRATING = 0
    
@router.get("/{store_id}")
def get_ratings(store_id: int):
    """
    Retrieve the list of reviews for a store.
    """
    with db.engine.begin() as connection:

        results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE store_id = :store_id"), {"store_id": store_id})
        reviews = []
        for row in results:
            reviews.append(
                {
                    "account": row.account_name,
                    "rating": row.rating,
                    "description": row.description
                }
            )

    return reviews

@router.get("/rating/{id}")
def get_specific_rating(id: int):
    """
    A review for a thrift store of reviews for a store.
    """
    result = {}

    with db.engine.begin() as connection:

        results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE id = :id"), {"id": id})
        review = results.fetchone()
        if review:
            result = {
                "account": review.account_name,
                "rating": review.rating,
                "description": review.description
            }

    return result
             
@router.post("/{store_id}")
def create_review(store_id: int, new_review: Review):
    """
    Creates new thrift review in website.
    """
    if new_review.rating > MAXRATING or new_review.rating < MINRATING:
        return "invalid rating: rating must be between 0 and 5"

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO reviews
                (account_name, rating, description, store_id)
                VALUES(:account_name, :rating, :description, :store_id)
                RETURNING id,  account_name, rating, description, store_id
                """
            ),
            [{"account_name": new_review.name, "rating": new_review.rating, "description": new_review.description, "store_id": store_id}]
        )
        result = result.fetchone()
    return {"id":result.id, "account_name": result.account_name, "rating": result.rating, "description": result.description, "store_id": result.store_id}

@router.post("/{id}")
def reply_review(id: int, new_reply: Reply):

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO replies
                (review_id, account_name, description)
                VALUES(:review_id, :account_name, :description)
                RETURNING id, review_id, account_name, description
                """
            ),
            [{ "review_id": id, "account_name": new_reply.name, "description": new_reply.description}]
        )
        result = result.fetchone()

    return {"id":result.id, "review_id":result.review_id, "account_name": result.account_name, "description": result.description}

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

@router.get("/search/{store_id}")
def sorted_reviews(store_id: int,
                   upper_rating: int = 5, 
                   lower_rating: int = 0, 
                   customer_name: str = "",
                   sort_order: search_sort_order = search_sort_order.desc):
    reviews = []
    if upper_rating > MAXRATING or lower_rating < MINRATING or lower_rating > upper_rating:
        return "invalid rating paramaters"
    with db.engine.begin() as connection:
        search_query = (sqlalchemy.select(
            db.reviews.c.id,
            db.reviews.c.account_name,
            db.reviews.c.rating,
            db.reviews.c.description,
        ).select_from(db.reviews)
        .where(db.reviews.c.store_id == store_id)
        .where(db.reviews.c.rating.between(lower_rating, upper_rating)))

        # sort query based on asc or desc and name
        if sort_order == search_sort_order.asc:
            search_query = search_query.order_by(db.reviews.c.rating.asc())
        if sort_order == search_sort_order.desc:
            search_query = search_query.order_by(db.reviews.c.rating.desc())
        if customer_name != "":
            search_query = search_query.where(db.reviews.c.account_name.ilike(f"%{customer_name}%"))

        result = connection.execute(search_query)
    reviews = [
        {
            "id": row.id,
            "account_name": row.account_name,
            "rating": row.rating,
            "description": row.description     
        }
        for row in result
    ]
    return reviews