from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)
class Description(BaseModel):
    description: str

@router.delete("/reset/{store_id}")
def reset(store_id: int):
    """
    a call to reset reviews will delete all reviews under a specific store
    """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM reviews WHERE store_id=:id"), {"id": store_id})

    return "OK"

@router.delete("/review/{review_id}")
def delete_review(review_id: int): 
    """
    a call to delete a specific review
    """
    print(review_id)
    with db.engine.begin() as connection: 
        connection.execute(sqlalchemy.text("DELETE FROM reviews WHERE id=:rev_id"), {"rev_id": review_id})
    return "OK"


@router.post("/update/description/{store_id}")
def update_descriptions(store_id: int, desc: Description):
    """ 
    a call to update descriptions for a store will add the admin description
    to database
    """

    with db.engine.begin() as connection: 
        connection.execute(sqlalchemy.text("UPDATE stores SET type=:desc WHERE id=:id"), {"desc": desc.description, "id": store_id})
    return "OK"