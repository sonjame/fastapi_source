from datetime import datetime

from pydantic import BaseModel, PositiveInt,ValidationError,Field,StringConstraints
from typing import Annotated,Literal
from annotated_types import Gt,Ge,Le

# todo 1개
class TodoItem(BaseModel):
    id:int
    title:str
    completed:bool
    important:bool