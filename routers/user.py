from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas import User
from jwt_manager import create_token

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)    
    else:
        return JSONResponse(content={"message": "Wrong credentials"}, status_code=401)