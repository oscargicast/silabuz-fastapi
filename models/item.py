from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Enum
from schemas.item import StatusItem


class ItemModel(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    status = Column(Enum(StatusItem))