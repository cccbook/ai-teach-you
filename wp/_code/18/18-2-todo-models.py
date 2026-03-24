from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TodoStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None

class TodoInDB(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Todo(TodoInDB):
    pass
