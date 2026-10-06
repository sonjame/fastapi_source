from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from repository.database import get_db
from services.comment import comment_create, comment_delete, comment_update
from schemas.comment import CommnetCreate, CommnetUpdate
from exceptions.board import CommentNotFoundException

# 화면단 요청 처리

comment_router = APIRouter(tags=["Comments"])

@comment_router.post("",response_model=dict)
async def post_comment(data:CommnetCreate, db:Session=Depends(get_db)):
    comment = comment_create(data,db=db)
    return {"message":f"comment{comment.comment_id}번 등록 성공"}



# /1 + put + 수정데이터
@comment_router.put("/{comment_id}",response_model=dict)
async def put_comment(comment_id:int, data:CommnetUpdate, db:Session=Depends(get_db)):
    
    try:
        id = comment_update(comment_id=comment_id, data=data, db=db)
    except CommentNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='수정할 comment 가 없습니다.')

    return {"message":f"comment {id} 번 수정 성공"}


@comment_router.delete("/{comment_id}",response_model=dict)
async def delete_comment(
    comment_id:int,  db:Session=Depends(get_db)
):
    try:
         comment_delete(comment_id=comment_id, db=db)
    except CommentNotFoundException:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='삭제할 comment 가 없습니다.')

    return {"message":f"comment {id} 번 삭제 성공"}
