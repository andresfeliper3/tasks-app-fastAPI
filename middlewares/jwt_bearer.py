from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

from db.database import get_db
from models.model import User as UserModel


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        auth = await super().__call__(request)
        token_data = validate_token(auth.credentials)

        db_user = db.query(UserModel).filter(UserModel.email == token_data['email']).first()

        if not db_user:
            raise HTTPException(status_code=403, detail="Wrong credentials")

        return auth
