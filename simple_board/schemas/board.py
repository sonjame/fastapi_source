# 게시글 삽입 : userId, title, body
# 게시글 조회 : userId, title, body, id

from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    user_id:int
    name:str

class CommentResponse(BaseModel):
    comment_id:int 
    body: str
    user_id: int
    # 댓글 작성자 정보
    user:UserResponse
    board_id: int
    created_at: datetime


class BoardCreate(BaseModel):
    user_id: int
    title:str
    contents:str


class BoardUpdate(BaseModel):
    title:str | None = None
    contents:str | None = None

class BoardResponse(BaseModel):
    id: int
    title:str
    contents:str
    user_id: int
    created_at:datetime
    # 게시글 작성자 이름
    user: UserResponse
    # 댓글목록
    comments:list[CommentResponse]

class BoardPageResponse(BaseModel):
    items:list[BoardResponse]
    total:int
    page:int
    size:int
    total_pages: int


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body : str

