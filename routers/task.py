from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from db.database import redis_conn

from schemas.task import Task
from db.database import get_db
from middlewares.jwt_bearer import JWTBearer
from services.task import TaskService

import json

task_router = APIRouter(prefix='/task', tags=['tasks'])

# Define the time limit for data stored in Redis (in seconds)
REDIS_TIME_LIMIT = 3600  # Set to 1 hour


@task_router.get('/', response_model=List[Task], status_code=200)
def get_tasks(db=Depends(get_db)) -> List[Task]:
    results = TaskService(db).get_tasks()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)


@task_router.get('/{id}', response_model=Task)
def get_task_by_id(id: int = Path(ge=1), db=Depends(get_db)) -> Task:
    # Use Redis to store and retrieve data
    task_key = f'task:{id}'
    if redis_conn.exists(task_key):
        result = redis_conn.get(task_key)
        result = jsonable_encoder(result)
    else:
        result = TaskService(db).get_task_by_id(id)
        if not result:
            return JSONResponse(
                content={"message": "Not found"}, status_code=400)
        redis_conn.set(task_key, json.dumps(jsonable_encoder(result)))
        # Set the time limit for the task key
        redis_conn.expire(task_key, REDIS_TIME_LIMIT)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@task_router.get('/category/{category_id}', response_model=List[Task])
def get_tasks_by_category(category_id: int, db=Depends(get_db)) -> List[Task]:
    result = TaskService(db).get_tasks_by_category(category_id)
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@task_router.post('/', response_model=dict)
def add_task(task: Task, db=Depends(get_db)) -> dict:
    # Use Redis to store data
    result = TaskService(db).add_task(task)
    result_json = jsonable_encoder(result)
    task_key = f'task:{result_json["id"]}'
    redis_conn.set(task_key, json.dumps(jsonable_encoder(result)))
    # Set the time limit for the task key
    redis_conn.expire(task_key, REDIS_TIME_LIMIT)
    redis_conn.delete('tasks')  # Delete the "tasks" key to update the data

    return JSONResponse(content=jsonable_encoder(result), status_code=201)


@task_router.put('/{id}', response_model=dict)
def update_task(id: int, updated_task: Task, db=Depends(get_db)) -> dict:
    result = TaskService(db).get_task_by_id(id)
    if not result:
        return JSONResponse(content={"message": "Not found"}, status_code=404)

    TaskService(db).update_task(id, updated_task)
    task_key = f'task:{id}'
    # Delete the key of the updated object in Redis
    redis_conn.delete(task_key)

    return JSONResponse(content={"message": "Task updated"}, status_code=200)


@task_router.delete('/{id}', response_model=dict)
def delete_task(id: int, db=Depends(get_db)) -> dict:
    result = TaskService(db).get_task_by_id(id)
    if not result:
        return JSONResponse(
            content={"message": "Task not found"}, status_code=404)

    result = TaskService(db).delete_task(id)
    task_key = f'task:{id}'
    # Delete the key of the deleted object in Redis
    redis_conn.delete(task_key)

    return JSONResponse(
        content={"message": "Task has been deleted"}, status_code=200)


@task_router.delete('/all', response_model=dict)
def delete_all_tasks(db=Depends(get_db)) -> dict:
    TaskService(db).delete_all_tasks()
    redis_conn.delete('tasks')  # Delete the "tasks" key in Redis

    return JSONResponse(
        content={"message": "All tasks deleted"}, status_code=200)
