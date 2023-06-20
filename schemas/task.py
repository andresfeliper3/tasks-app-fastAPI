from pydantic import BaseModel, Field
from typing import Optional
from utils.time import today_year


class Task(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(max_length=500)
    year: int = Field(le=today_year)  # <= current year
    category_id: int
    creator_id: int
    in_charge_id: int

    class Config:
        schema_extra = {
            "example": {
                "title": "My task",
                "content": "Content...",
                "year": today_year,
                "category_id": 1,
                "creator_id": 1,
                "in_charge_id": 1
            }
        }
