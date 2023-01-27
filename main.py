from fastapi import FastAPI, Body, Query
from enum import Enum
from typing import Union, Optional
from pydantic import BaseModel
from config.database import engine, Base
from models.item import Item


app = FastAPI(
    title='Silabuz',
    version='0.0.1',
)

Base.metadata.create_all(bind=engine)


class StatusItem(str, Enum):
    good = "good"
    bad = "bad"


items = [{
    "id": 1,
    "name": "mesa",
    "price": 70.5,
    "status": StatusItem.good,
}, {
    "id": 2,
    "name": "silla",
    "price": 50.5,
    "status": StatusItem.bad,
}, {
    "id": 3,
    "name": "pc",
    "price": 1050,
    "status": StatusItem.bad,
}, {
    "id": 4,
    "name": "laptop",
    "price": 2050,
    "status": StatusItem.good,
}]


class Item(BaseModel):
    id: Optional[int]
    name: str
    price: float
    status: StatusItem = StatusItem.good


@app.get("/")
def read_root():
    return {"message": "Chau mundo"}

# CRUD: Create, Read, Update, Delete.
# GET, POST, PUT, PATCH, DELETE.

@app.get("/items/", tags=["item"])
async def get_items(status: Union[StatusItem, None] = None, search: Union[str, None] = None):
    """Returns a list of all items."""
    if not status:
        return items
    filtered_items = []
    for item in items:
        if status == item.get("status"):
            filtered_items.append(item)
    return filtered_items


@app.get("/items/{item_id}", tags=["item"])
async def get_item(item_id: int):
    """Return the detail of an item."""
    for item in items:
        if item_id == item.get("id"):
            return item


@app.post("/items/", tags=["item"])
async def create_item(new_item: Item, add_depreciation: bool = Body(default=False)):
    """Create an item."""
    if new_item.id is None:
        new_item.id = len(items) + 1
    if add_depreciation:
        new_item.price = new_item.price * 0.7
    return new_item


@app.put("/items/{item_id}", tags=["item"])
async def create_item(item_id: int):
    """Create an item."""
    return


@app.delete("/items/", tags=["item"])
async def create_item(item_id: int):
    """Create an item."""
    return