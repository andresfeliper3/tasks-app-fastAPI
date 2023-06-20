from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

from db.database import get_db
from models.model import User as UserModel


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        # Call the parent class method to authenticate the request using the Bearer token
        auth = await super().__call__(request)
        
        # Validate the token and extract its data
        token_data = validate_token(auth.credentials)
        
        # Retrieve the user from the database based on the token's email
        db_user = db.query(UserModel).filter(UserModel.email == token_data['email']).first()

        # If no user is found, raise an HTTPException with status code 403 (Forbidden)
        if not db_user:
            raise HTTPException(status_code=403, detail="Wrong credentials")

        # Return the authenticated user
        return auth
