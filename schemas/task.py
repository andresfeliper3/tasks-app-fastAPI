from pydantic import BaseModel, Field
from typing import Optional

import datetime
today = datetime.date.today()


class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(max_length=500)
    year: int = Field(le=today.year) # <= current year
    category: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My task",
                "content": "Content...",
                "year": today.year,
                "category": "Default"
            }
        }
        