from pydantic import BaseModel, EmailStr, Field, validator
from utils.time import today_year


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class RegisterUser(BaseModel):
    firstname: str
    lastname: str
    year_of_birth: int = Field(le=today_year)  # <= current year
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, password):
        # Apply password restrictions
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if password.isalpha():
            raise ValueError(
                'Password must contain at least one numeric or special character')
        return password
