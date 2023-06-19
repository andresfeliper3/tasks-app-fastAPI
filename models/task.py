from sql_app.database import Base
from sqlalchemy import Column, Integer, String

class Task(Base):
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    year = Column(Integer)
    category = Column(String)