from enum import Enum
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from sqlalchemy import text

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

        # # performance testing query
        # performance_results = connection.execute(text(
        #         """
        #         EXPLAIN ANALYZE
        #         SELECT account_name, rating, description FROM reviews WHERE store_id = :store_id
        #         """),{"store_id": store_id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        results = connection.execute(sqlalchemy.text("SELECT id, account_name, rating, description FROM reviews WHERE store_id = :store_id"), {"store_id": store_id})
        reviews = []
        for row in results:
            reviews.append(
                {   
                    "rating_id": row.id,
                    "account": row.account_name,
                    "rating": row.rating,
                    "description": row.description
                }
            )

    return reviews

@router.get("/replies/{rating_id}")
def get_replies(review_id: int):
    """
    Retrieve the list of replies for a specific rating
    """
    with db.engine.begin() as connection:

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

        results = connection.execute(sqlalchemy.text("SELECT id, review_id, account_name, description FROM replies WHERE review_id = :review_id"), {"review_id": review_id})
        replies = []
        for row in results:
            replies.append(
                {   
                    "id": row.id,
                    "review_id": row.review_id,
                    "account": row.account_name,
                    "description": row.description
                }
            )

    return replies

@router.get("/rating/{id}")
def get_specific_rating(id: int):
    """
    Gets specific rating given rating_id
    """
    result = {}
    with db.engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:
        trans = connection.begin()

        try:

            # # performance testing query 
            # performance_results = connection.execute(text(
            #     """
            #     EXPLAIN ANALYZE
            #     SELECT account_name, rating, description FROM reviews WHERE id = :id FOR UPDATE"""),{"id": id})
            # query_plan = performance_results.fetchall()
            # for row in query_plan:
            #     print(row)

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

             
@router.post("/review/{store_id}")
def create_review(store_id: int, new_review: Review):
    """
    Creates new thrift review in website.
    """
    if new_review.rating > MAXRATING or new_review.rating < MINRATING:
        return "invalid rating: rating must be between 0 and 5"

    with db.engine.begin() as connection:

        # # performance testing query 
        # performance_results = connection.execute(text(
        #     """
        #     EXPLAIN ANALYZE
        #     INSERT INTO reviews
        #     (account_name, rating, description, store_id)
        #     VALUES(:account_name, :rating, :description, :store_id)
        #     RETURNING id,  account_name, rating, description, store_id
        #     """),[{"account_name": new_review.name, "rating": new_review.rating, "description": new_review.description, "store_id": store_id}])
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

@router.post("/reply/{id}")
def reply_review(id: int, new_reply: Reply):
    """
    Creates new thrift review in website.
    """
    
    with db.engine.begin() as connection:

        # # performance testing query 
        # performance_results = connection.execute(text(
        #     """
        #     EXPLAIN ANALYZE
        #     INSERT INTO replies
        #         (review_id, account_name, description)
        #         VALUES(:review_id, :account_name, :description)
        #         RETURNING id, review_id, account_name, description
        #     """),[{ "review_id": id, "account_name": new_reply.name, "description": new_reply.description}])
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
            {"review_id": id}
        )
        if result.scalar_one() == 0:
            return "Review does not exist"

        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO replies
                (review_id, account_name, description)
                VALUES(:review_id, :account_name, :description)
                RETURNING id, review_id, account_name, description
                """
            ),
            { "review_id": id, "account_name": new_reply.name, "description": new_reply.description}
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

        # # performance testing query
        # performance_results = connection.execute(text(
        #     """
        #     EXPLAIN ANALYZE
        #     SELECT id, account_name, rating, description
        #     FROM reviews
        #     WHERE reviews.store_id = :store_id and reviews.rating BETWEEN 4 and 5
        #     ORDER BY reviews.rating desc
        #     """
        # ), {"store_id": store_id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

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



@router.put("/update/{review_id}")
def update_review(review_id: int, updated_review: Review):
    """
    Update an existing review
    """
    connection = db.engine.connect().execution_options(isolation_level="READ COMMITTED")
    if updated_review.rating > MAXRATING or updated_review.rating < MINRATING:
        return "invalid rating: rating must be between 0 and 5"

    try:
        with connection.begin():
            # Check if the review with the given ID exists
            existing_review = connection.execute(
                sqlalchemy.text("SELECT * FROM reviews WHERE id = :review_id FOR UPDATE"), {"review_id": review_id}
            ).fetchone()

            if not existing_review:
                return "Review not found"

            # # performance testing query
            # performance_results = connection.execute(text(
            #     """
            #         EXPLAIN ANALYZE
            #         UPDATE reviews
            #         SET account_name = :account_name, rating = :rating, description = :description WHERE id = :review_id
            #         """
            # ), {
            #         "review_id": review_id,
            #         "account_name": updated_review.name,
            #         "rating": updated_review.rating,
            #         "description": updated_review.description,
            #     })
            # query_plan = performance_results.fetchall()
            # for row in query_plan:
            #     print(row)

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
