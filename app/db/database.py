from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://db_tasks_api_in_fastapi_user:R19EOCY7Bgy1kVUoWxQxDA6NSOuMDTr9@dpg-ci87p4p8g3n3vm3l03bg-a.ohio-postgres.render.com/db_tasks_api_in_fastapi'


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
