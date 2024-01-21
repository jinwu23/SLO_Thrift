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
    Retrieve the list of reviews for a specific store.
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

@router.get("/average/{store_id}")
def get_rating_averages(store_id: int):
    """
    Get the average rating and rank of store based on rating
    """
    with db.engine.begin() as connection:
        stores = []
        result = connection.execute(
            sqlalchemy.text(
                """
                WITH rankedaverage AS (
                    SELECT RANK() OVER (ORDER BY COALESCE(ROUND(AVG(reviews.rating), 2), 0) DESC) as store_rank, 
                    stores.name as store_name, 
                    COALESCE(ROUND(AVG(reviews.rating), 2), 0) as avg_rating,
                    stores.id as sid
                    FROM stores
                    JOIN reviews ON reviews.store_id = stores.id
                    GROUP BY sid, store_name
                    ORDER BY avg_rating DESC
                )
                SELECT store_rank, store_name, avg_rating
                FROM rankedaverage
                WHERE sid = :store_id
                """
            ),
            {"store_id": store_id}
        )
        data = result.fetchone()
    
    return dict(store_rank=data.store_rank, store_name=data.store_name, average_rating=data.avg_rating)

@router.get("/rating/{id}")
def get_specific_rating(id: int):
    """
    Gets specific rating given rating_id
    """
    result = {}
    with db.engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:
        trans = connection.begin()

        try:
            # Use "FOR UPDATE" to lock the selected rows
            results = connection.execute(sqlalchemy.text("SELECT account_name, rating, description FROM reviews WHERE id = :id FOR UPDATE"), {"id": id})
            review = results.fetchone()

            if review:
                result = {
                    "account": review.account_name,
                    "rating": review.rating,
                    "description": review.description
                }

            # Commit the transaction explicitly
            trans.commit()

        except Exception as e:
            trans.rollback()
            raise e

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
    """
    Creates new thrift review in website.
    """
    
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
    """
    Sorts the reviews listed.
    """
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



@router.post("/update/{review_id}")
def update_review(review_id: int, updated_review: Review):
    """
    Update an existing review
    """
    connection = db.engine.connect().execution_options(isolation_level="READ COMMITTED")

    try:
        with connection.begin():
            # Check if the review with the given ID exists
            existing_review = connection.execute(
                sqlalchemy.text("SELECT * FROM reviews WHERE id = :review_id FOR UPDATE"), {"review_id": review_id}
            ).fetchone()

            if not existing_review:
                return "Review not found"

            # Update the review
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE reviews
                    SET account_name = :account_name, rating = :rating, description = :description WHERE id = :review_id
                    """
                ),
                {
                    "review_id": review_id,
                    "account_name": updated_review.name,
                    "rating": updated_review.rating,
                    "description": updated_review.description,
                },
            )

    except Exception as e:
        raise e

    return "OK"