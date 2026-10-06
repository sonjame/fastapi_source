# CRUD
from sqlalchemy.orm import Session
from schemas.comment import CommnetCreate, CommnetUpdate
from repository.models.comment import Comment
from exceptions.board import CommentNotFoundException


# 댓글 등록
def comment_create(data:CommnetCreate, db:Session):
    comment = Comment(body=data.body, user_id=data.user_id, board_id=data.board_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# 댓글 수정
def comment_update(comment_id:int, data:CommnetUpdate, db:Session):
    # 수정할 대상 찾기
    comment = db.get(Comment, comment_id)

    if comment is None:
        raise CommentNotFoundException

    # 수정작업
    if data.body is not None:
        comment.body = data.body

    db.commit()
    return comment_id


# 댓글 삭제
def comment_delete(comment_id:int, db:Session):
    # 삭제할 대상 찾기
    comment = db.get(Comment, comment_id)

    if comment is None:
            raise CommentNotFoundException

    db.delete(comment)
    db.commit()
