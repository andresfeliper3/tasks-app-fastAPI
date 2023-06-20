from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from schemas.task import Task
from db.database import get_db
from middlewares.jwt_bearer import JWTBearer
from services.task import TaskService

task_router = APIRouter(prefix='/task', tags=['tasks'])


# , dependencies=[Depends(JWTBearer())])
@task_router.get('/', response_model=List[Task], status_code=200)
def get_tasks(db=Depends(get_db)) -> List[Task]:
    results = TaskService(db).get_tasks()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)


@task_router.get('/{id}', response_model=Task)
def get_task_by_id(id: int = Path(ge=1), db=Depends(get_db)) -> Task:
    result = TaskService(db).get_task_by_id(id)
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=400)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@task_router.get('/', response_model=List[Task])
def get_tasks_by_category(category: str = Query(
        min_length=3), db=Depends(get_db)) -> List[Task]:
    result = TaskService(db).get_tasks_by_category(category)
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@task_router.post('/', response_model=dict)
def add_task(task: Task, db=Depends(get_db)) -> dict:
    result = TaskService(db).add_task(task)
    return JSONResponse(content=jsonable_encoder(result), status_code=201)


@task_router.put('/{id}', response_model=dict)
def update_task(id: int, updated_task: Task, db=Depends(get_db)) -> dict:
    result = TaskService(db).get_task_by_id(id)
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)
    TaskService(db).update_task(id, updated_task)
    return JSONResponse(content={"message": "Task updated"}, status_code=200)


@task_router.delete('/{id}', response_model=dict)
def delete_task(id: int, db=Depends(get_db)) -> dict:
    result = TaskService(db).get_task_by_id(id)
    if not result:
        return JSONResponse(
            content={"message": "Task not found"}, status_code=404)
    result = TaskService(db).delete_task(id)
    return JSONResponse(
        content={"message": "Task has been deleted"}, status_code=200)


@task_router.delete('/all', response_model=dict)
def delete_all_tasks(db=Depends(get_db)) -> dict:
    TaskService(db).delete_all_tasks()
    return JSONResponse(
        content={"message": "All tasks deleted"}, status_code=200)
