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
    address: str
    rating: int
    description: str

@router.get("/store/", tags=["store"])
def get_store():
    print("ok")