
from enum import Enum
from pydantic import BaseModel, Field
from typing import Union, Optional


class StatusItem(str, Enum):
    good = "good"
    bad = "bad"


class Item(BaseModel):
    id: Optional[int] = Field(ge=1)
    name: str = Field(min_length=1, max_length=20)
    price: float
    status: StatusItem = StatusItem.good

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "celular",
                "price": 705.50,
                "status": StatusItem.bad,
            }
        }


# Output schema.
class FullItem(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=20)
    price: float
    status: StatusItem


class PutItem(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    price: float
    status: StatusItem


class CreateItem(PutItem):
    pass