from db.database import Base
from sqlalchemy import Column, Integer, String


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
