from config.database import engine, Base, Session
from fastapi import FastAPI, Body, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from models.item import ItemModel
from typing import Union, List
from fastapi.encoders import jsonable_encoder
from schemas.item import (
    StatusItem,
    Item,
    FullItem,
    PutItem,
    CreateItem,
)


app = FastAPI(
    title='Silabuz',
    version='0.0.1',
)

Base.metadata.create_all(bind=engine)

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



@app.get("/")
def read_root():
    return JSONResponse(status_code=201, content={"message": "Chau mundo"})
    # return HTMLResponse('<h1>Hello world</h1>')

# CRUD: Create, Read, Update, Delete.
# GET, POST, PUT, PATCH, DELETE.

@app.get("/items/", response_model=List[FullItem],tags=["item"])
async def get_items(status: Union[StatusItem, None] = None, search: Union[str, None] = Query(max_length=20, default=None)) -> List[FullItem]:
    """Returns a list of all items."""
    db = Session()
    if status:
        results = db.query(ItemModel).filter(ItemModel.status == status).all()
    else:
        results = db.query(ItemModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(results))


@app.get("/items/{item_id}", response_model=FullItem, tags=["item"])
async def get_item(item_id: int = Path(ge=1)) -> FullItem:
    """Return the detail of an item."""
    db = Session()
    result = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not result:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Item not found",
            },
        )
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.post("/items/", response_model=FullItem, status_code=201, tags=["item"])
async def create_item(new_item: CreateItem, add_depreciation: bool = Body(default=False)) -> FullItem:
    """Create an item."""
    db = Session()
    if add_depreciation:
        new_item.price = new_item.price * 0.7
    new = ItemModel(**new_item.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return jsonable_encoder(new)
    # return {
    #     "id": new.id,
    #     "name": new.name,
    #     "price": new.price,
    #     "status": new.status,
    # }
    # return JSONResponse(status_code=201, content=)


@app.put("/items/{item_id}", response_model=FullItem, tags=["item"])
async def put_item(updated_item: PutItem, item_id: int = Path(ge=1)) -> FullItem:
    """Create an item."""
    # Check if the item exists.
    db = Session()
    result = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    # If exists.
    result.name = updated_item.name
    result.price = updated_item.price
    result.status = updated_item.status
    db.commit()
    return JSONResponse(
        status_code=200,
        content=f'Item with id {item_id} updated!',
    )


@app.delete("/items/", tags=["item"])
async def delete_item(item_id: int):
    """Create an item."""
    # Check if the item exists.
    db = Session()
    result = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    # If exists.
    db.delete(result)
    db.commit()
    return JSONResponse(
        status_code=200,
        content=f'Item with id {item_id} deleted!',
    )