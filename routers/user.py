from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.user import LoginUser, RegisterUser
from utils.jwt_manager import create_token
import bcrypt
from sqlalchemy.orm import Session
from db.database import get_db
from models.model import User as UserModel


user_router = APIRouter()


@user_router.post('/login', tags=['auth'])
def login(user: LoginUser, db: Session = Depends(get_db)):
    # Query the database for the user with the provided email
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if db_user:
        # Verify the password against the hashed password stored in the
        # database
        if bcrypt.checkpw(user.password.encode('utf-8'),
                          db_user.password.encode('utf-8')):
            token: str = create_token(user.dict())
            return JSONResponse(content=token, status_code=200)

    return JSONResponse(
        content={"message": "Wrong credentials"}, status_code=401)


@user_router.post('/register', tags=['auth'])
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # Encrypt the password
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt())

    # Create a new user with the encrypted password
    new_user = UserModel(
        firstname=user.firstname,
        lastname=user.lastname,
        year_of_birth=user.year_of_birth,
        email=user.email,
        # Store the hashed password as a string
        password=hashed_password.decode('utf-8')
    )

    # Save the new user to the database
    db.add(new_user)
    db.commit()

    # Return a success response
    return JSONResponse(
        content={"message": "User registered successfully"}, status_code=201)
