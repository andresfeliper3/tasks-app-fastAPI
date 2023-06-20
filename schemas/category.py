from pydantic import BaseModel, Field
from typing import Optional


class Category(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=100)
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "My category",
                "description": "This is a description..."
            }
        }
