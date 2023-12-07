from enum import Enum
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db
from sqlalchemy import asc, desc, text, func

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
        
        # # performance testing query
        # performance_results = connection.execute(text(
        #         """
        #         EXPLAIN ANALYZE
        #         SELECT 
        #             stores.id as id, 
        #             stores.name as name, 
        #             stores.address as address, 
        #             stores.type as type, 
        #             AVG(reviews.rating) as rating 
        #         FROM stores 
        #         LEFT JOIN reviews on reviews.store_id = stores.id 
        #         GROUP BY stores.id
        #         ORDER BY stores.id asc
        #         """))
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    stores.id as id, 
                    stores.name as name, 
                    stores.address as address, 
                    stores.type as type, 
                    round(coalesce(AVG(reviews.rating), 0),2) as rating 
                FROM stores 
                LEFT JOIN reviews on reviews.store_id = stores.id 
                GROUP BY stores.id
                ORDER BY stores.id asc
                """))
        results = results.fetchall()
        for row in results:
            stores_arr.append(
                {   
                    "id": row.id,
                    "name": row.name,
                    "rating": row.rating,
                    "address": row.address,
                    "type": row.type,
                })
    print("get_stores")
    return stores_arr

@router.get("/{id}")
def get_specific_store(id: int):
    """
    Get a specific thrift store given id
    """
    with db.engine.begin() as connection:
        # # performance testing query
        # performance_results = connection.execute(text(
        #         """
        #         EXPLAIN ANALYZE
        #         SELECT stores.id, stores.name, 
        #         stores.address, stores.type, AVG(reviews.rating)
        #         as rating FROM stores 
        #         LEFT JOIN reviews on reviews.store_id = stores.id 
        #         WHERE stores.id = :id 
        #         GROUP BY stores.id
        #         """), 
        #         {"id": id})
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT stores.id, stores.name, 
                stores.address, stores.type, 
                round(AVG(reviews.rating), 2)as rating FROM stores 
                LEFT JOIN reviews on reviews.store_id = stores.id 
                WHERE stores.id = :id 
                GROUP BY stores.id
                """), 
                {"id": id})
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

        # # performance testing query
        # performance_results = connection.execute(text(
        #         """
        #         BEGIN;
        #         EXPLAIN ANALYZE
        #         INSERT INTO stores
        #         (name, address, type)
        #         VALUES(:name, :address, :type) 
        #         RETURNING id;
        #         """), 
        #         [{"name": new_store.name, 
        #           "address": new_store.address, 
        #           "type": new_store.type}])
        # query_plan = performance_results.fetchall()
        # for row in query_plan:
        #     print(row)

        result = connection.execute(
            sqlalchemy.text(
                """
                BEGIN;
                INSERT INTO stores
                (name, address, type)
                VALUES(:name, :address, :type) 
                RETURNING id;
                """
            ),
            [{"name": new_store.name, 
              "address": new_store.address, 
              "type": new_store.type}])
        store_id = result.scalar()
        print(store_id)
        # print("trying to insert into reviews")
        # connection.execute(
        #     sqlalchemy.text(
        #         """
        #         INSERT INTO reviews
        #         (account_name, rating, description, store_id)
        #         VALUES(:account_name, :rating, :description, :store_id);
        #         COMMIT;
        #         """
        #     ),
        # {"account_name": "init", 
        #  "rating": None, 
        #  "description": "init", 
        #  "store_id": store_id})
        
    return f"New store created, id: {store_id}"

@router.put("/{store_id}")
def update_store(store_id: int, attribute: str, new_attribute: str):
    """
    Updates the name, address, or type of a specific store
    """

    if attribute not in ("name", "address", "type"):
        return "Attribute must be either: name, address, or type"
    if attribute == "name":
        query = """
                UPDATE stores
                SET name = :new_attribute
                where id = :id
                """
    elif attribute == "address":
        query = """
                UPDATE stores
                SET address = :new_attribute
                where id = :id
                """
    else:
        query = """
                UPDATE stores
                SET type = :new_attribute
                where id = :id
                """
    # # performance testing query
    # with db.engine.begin() as connection:
    #     performance_results = connection.execute(text(
    #         """ 
    #             EXPLAIN ANALYZE
    #             UPDATE stores
    #             SET type = :new_attribute
    #             where id = :id
    #             """
    #     ), [{"id": store_id, "attribute": attribute, "new_attribute": new_attribute}])
    #     query_plan = performance_results.fetchall()
    #     for row in query_plan:
    #         print(row)

    with db.engine.begin() as connection:
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

        connection.execute(
            sqlalchemy.text(query),
            [{"id": store_id, "attribute": attribute, "new_attribute": new_attribute}]
        )
    return "OK"

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

class search_sort_options(str, Enum):
    rating = "average_rating"
    name = "name"
    address = "address"
    type = "type"

@router.get("/search/{store_id}")
def sorted_stores(
                    sort_options: search_sort_options = search_sort_options.rating,
                    sort_order: search_sort_order = search_sort_order.desc
                    ):
    with db.engine.begin() as connection:
        search_query = (
            sqlalchemy.select(
                db.stores.c.id,
                db.stores.c.name,
                db.stores.c.address,
                db.stores.c.type,
                func.round(func.coalesce(func.avg(db.reviews.c.rating), 0), 2).label('average_rating')
            )
            .select_from(db.stores)
            .outerjoin(db.reviews, db.stores.c.id == db.reviews.c.store_id)
            .group_by(
                db.stores.c.id,
            )
        )

        # sort query based on asc or desc and name
        if sort_order == search_sort_order.asc:
            search_query = search_query.order_by(asc(sort_options))
        if sort_order == search_sort_order.desc:
            search_query = search_query.order_by(desc(sort_options))

        result = connection.execute(search_query)
    reviews = [
        {
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "type": row.type,
            "average_rating": row.average_rating
        }
        for row in result
    ]
    return reviews