
from pydantic import BaseModel

class TaskCreate(BaseModel):    
    text:str
    done:bool

class TaskUpdate(BaseModel):    
    text:str | None = None
    done:bool | None = None

class TaskResponse(TaskCreate):
    id:int

class TaskPageResponse(BaseModel):
    items: list[TaskResponse]
    total:int
    total_pages: int
    page: int
    size: int

