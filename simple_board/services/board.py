# CRUD 작업
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repository.models.board import Board, Board_Views
from repository.models.comment import Comment
from schemas.board import BoardCreate, BoardUpdate
from exceptions.board import BoardNotFoundException
from repository.models.user import User
from exceptions.user import UserCredentialsExcepation
import math

def create(db:Session, data:BoardCreate, current_user:User):
    # 스키마 => 테이블 연결 모델
    board = Board(title=data.title, contents=data.contents, user_id=current_user.user_id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

def update(db: Session, id: int, data: BoardUpdate, current_user: User):
    # 수정할 대상 찾기
    board = db.get(Board, id)

    if board is None:
        BoardNotFoundException

    # 로그인 사용자 == 작성자 아냐?
    if board.user_id != current_user.user_id:
        raise UserCredentialsExcepation

    # title만 수정 or contents 만 수정 or title, contents 둘다 수정
    if data.title is not None:
        board.title = data.title

    # contents만 수정
    if data.contents is not None:
        board.contents = data.contents

    db.commit()
    db.refresh(board)

    return id

# id 와 일치하는 board 하나 조회
# def select_one(db:Session, id:int):
#     board = db.get(Board, id)

#     if board is None:
#         BoardNotFoundException

#     return board


# 조회수 증가
def update_views(db: Session, board:Board, current_user:User):
    # Boards 테이블의 update views + 1
    # board_views 테이블 insert () => 동일한 값이 존재하는지 확인

    stmt = select(Board_Views).where(
        Board_Views.board_id == board.id, Board_Views.user_id == current_user.user_id
    )
    view = db.scalar(stmt)

    if view is None:
        board.views += 1

        board_view = Board_Views(board_id=board.id, user_id=current_user.user_id)
        db.add(board_view)
        db.commit()




# id와 일치하는 board 하나 조회 + 댓글 함께
def select_one(db:Session, id:int):

    stmt = (
        select(Board)
        .options(
            selectinload(Board.user), # 게시글 작성자 정보
            selectinload(Board.comments).selectinload(Comment.user), # 댓글+댓글작성자
        )
        .where(Board.id == id)
    )

    board = db.scalar(stmt)

    if board is None:
        raise BoardNotFoundException

    return board

def recentPosts(db:Session):
    # 최신게시물 4개 추출
    return db.query(Board).order_by(Board.created_at.desc()).limit(4).all()


# page,size 이용하는 전체조회 + 검색
def select_all(db:Session, page:int, size:int, criteria:str, keyword:str):
    # select * from boards order bu id desc limit 20,10
    query = db.query(Board)

    if keyword:
        if criteria == "tc":
            query = query.filter(Board.title.contains(keyword) | Board.contents.contains(keyword))
        elif criteria == "t":
            query = query.filter(Board.title.contains(keyword))
        elif criteria == "w":
            query = query.join(Board.user).filter(User.name.contains(keyword))

    # 전체 개수(페이지 수 알아내기 위해서)
    total = query.count()
    offset = (page - 1) * size
    boards = query.order_by(Board.id.desc()).offset(offset).limit(size).all()
    total_pages = math.ceil(total/size)

    return{
        "items":boards,
        "total":total,
        "page":page,
        "size":size,
        "total_pages":total_pages,
        "criteria" : criteria,
        "keyword": keyword,
    }

# 삭제
def delete(db:Session, id:int,  current_user:User):
    # 삭제할 대상 찾기
    board = db.get(Board, id)

    if board is None:
        BoardNotFoundException

    if board.user_id != current_user.user_id:
        raise UserCredentialsExcepation


    db.delete(board)
    db.commit()
    return id


