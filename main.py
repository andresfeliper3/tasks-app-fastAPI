from fastapi import FastAPI, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from starlette.requests import Request

from config import create_configuration_fastapi
from models import Task, User
from data import tasks

from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
create_configuration_fastapi(app)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Wrong credentials")
        

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
         response_model=List[Task], status_code=200, dependencies=[Depends(JWTBearer())])
def get_tasks() -> List[Task]:
    return JSONResponse(content=tasks, status_code=200)

@app.get('/tasks/{id}', tags=['tasks'], response_model = Task)
def get_task_by_id(id: int = Path(ge=1)) -> Task:
    for task in tasks:
        if task['id'] == id:
            return JSONResponse(content=task, status_code=200)
    return JSONResponse(content=[], status_code=400)

@app.get('/tasks/', tags=['tasks'], response_model = List[Task])
def get_tasks_by_category(category: str = Query(min_length=3)) -> List[Task]:
    data = [task for task in tasks if task['category'] == category]
    return JSONResponse(content=data, status_code=200)
    
@app.post('/tasks', tags=['tasks'], response_model=dict)
def add_task(task: Task) -> dict:
        tasks.append(task.dict())
        return JSONResponse(content={"message": "Task registered"}, status_code=201)
    
    
@app.put('/tasks/{id}', tags=['tasks'], response_model=dict)
def update_task(id: int, updated_task: Task) -> dict:
    for index, task in enumerate(tasks):
        if task['id'] == id:
            tasks[index] = updated_task.dict()
            return JSONResponse(content={"message": "Task updated"}, status_code=200)     
    return JSONResponse(content={"message": "Task not found"}, status_code=404)

@app.delete('/tasks/{id}', tags=['tasks'], response_model=dict)
def delete_task(id: int) -> dict:
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            return JSONResponse(content={"message": "Task deleted"}, status_code=200)     
    return JSONResponse(content={"message": "Task not found"}, status_code=404)     