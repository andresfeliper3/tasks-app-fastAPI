from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from config import create_configuration_fastapi
from schemas import User

from jwt_manager import create_token
from sql_app.database import  engine, Base

from middlewares.error_handler import ErrorHandler


app = FastAPI()
create_configuration_fastapi(app, middleware=ErrorHandler)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


