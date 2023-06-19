from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from config import create_configuration_fastapi
from schemas import User, Task

from jwt_manager import create_token
from sql_app.database import SessionLocal, engine, Base
from models.task import Task as TaskModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
create_configuration_fastapi(app, middleware=ErrorHandler)

Base.metadata.create_all(bind=engine)

    

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)    
    else:
        return JSONResponse(content={"message": "Wrong credentials"}, status_code=401)

@app.get('/tasks', tags=['tasks'], 
         response_model=List[Task], status_code=200)#, dependencies=[Depends(JWTBearer())])
def get_tasks() -> List[Task]:
    db = SessionLocal()
    results = db.query(TaskModel).all()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)

@app.get('/tasks/{id}', tags=['tasks'], response_model = Task)
def get_task_by_id(id: int = Path(ge=1)) -> Task:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=400)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    

@app.get('/tasks/', tags=['tasks'], response_model = List[Task])
def get_tasks_by_category(category: str = Query(min_length=3)) -> List[Task]:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.category == category).all()
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    
@app.post('/tasks', tags=['tasks'], response_model=dict)
def add_task(task: Task) -> dict:
    db = SessionLocal()
    new_task = TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    return JSONResponse(content={"message": "Task registered"}, status_code=201)
    
    
@app.put('/tasks/{id}', tags=['tasks'], response_model=dict)
def update_task(id: int, updated_task: Task) -> dict:
    db = SessionLocal()
    old_task = db.query(TaskModel).filter(TaskModel.id == id)
    
    if old_task.scalar():
        data = updated_task.dict()
        data['id'] = id
        old_task.update(data)
        db.commit()
        return JSONResponse(content={"message": "Task updated"}, status_code=200)
    return JSONResponse(content={"message": "Not found"}, status_code=404)
  

@app.delete('/tasks/{id}', tags=['tasks'], response_model=dict)
def delete_task(id: int) -> dict:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not result:   
        return JSONResponse(content={"message": "Task not found"}, status_code=404)     
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Task has been deleted"}, status_code=200)