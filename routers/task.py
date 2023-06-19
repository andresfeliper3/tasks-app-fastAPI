from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from schemas import Task

from sql_app.database import SessionLocal
from models.task import Task as TaskModel

from middlewares.jwt_bearer import JWTBearer


task_router = APIRouter()

@task_router.get('/tasks', tags=['tasks'], 
         response_model=List[Task], status_code=200)#, dependencies=[Depends(JWTBearer())])
def get_tasks() -> List[Task]:
    db = SessionLocal()
    results = db.query(TaskModel).all()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)

@task_router.get('/tasks/{id}', tags=['tasks'], response_model = Task)
def get_task_by_id(id: int = Path(ge=1)) -> Task:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=400)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    

@task_router.get('/tasks/', tags=['tasks'], response_model = List[Task])
def get_tasks_by_category(category: str = Query(min_length=3)) -> List[Task]:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.category == category).all()
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    
@task_router.post('/tasks', tags=['tasks'], response_model=dict)
def add_task(task: Task) -> dict:
    db = SessionLocal()
    new_task = TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    return JSONResponse(content={"message": "Task registered"}, status_code=201)
    
    
@task_router.put('/tasks/{id}', tags=['tasks'], response_model=dict)
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
  

@task_router.delete('/tasks/{id}', tags=['tasks'], response_model=dict)
def delete_task(id: int) -> dict:
    db = SessionLocal()
    result = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not result:   
        return JSONResponse(content={"message": "Task not found"}, status_code=404)     
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Task has been deleted"}, status_code=200)