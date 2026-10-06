# 타입 점검(pydantic)
from pydantic import BaseModel
from datetime import datetime


class CommnetCreate(BaseModel):
    body:str
    user_id:int
    board_id:int


class CommnetUpdate(BaseModel):
    body:str | None = None



