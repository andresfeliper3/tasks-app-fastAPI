from pydantic import BaseModel, Field
from typing import Optional

class Category(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=100)
    description: str
    
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My category",
                "description":"This is a description..."
            }
        }