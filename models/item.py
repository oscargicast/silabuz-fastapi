from config.database import Base
from sqlalchemy import Column, Integer, String, Float


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)