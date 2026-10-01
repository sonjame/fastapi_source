# 게시글 삽입 : userId, title, body
# 게시글 조회 : userId, title, body, id

from pydantic import BaseModel

class BoardInsert(BaseModel):
    userId: int
    title:str
    body:str

class Board(BoardInsert):
    id:int

class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body : str

