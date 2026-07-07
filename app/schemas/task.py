from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str
