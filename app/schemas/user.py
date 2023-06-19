from pydantic import BaseModel, EmailStr, Field, validator
from utils.time import today

class User(BaseModel):
    firstname: str
    lastname: str   
    year_of_birth: int = Field(le=today.year)  # <= current year
    email: EmailStr
    password: str 
    
    @validator('password')
    def validate_password(cls, password):
        # Aplica las restricciones a la contraseña
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if password.isalpha():
            raise ValueError('Password must contain at least one numeric or special character')
        return password
