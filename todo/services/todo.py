# database 작업 호출 : CRUD

# 테이블과 연결된 Todo

from repository.models.todo import Todo
from sqlalchemy.orm import Session
import math

# commit() : 

# C : insert
def create(todo:Todo, db:Session):
    db.add(todo)
    db.commit()
    # db에 저장된 최신 값을 다시 읽어서 현재 todo에 반영
    # id, created_at, updated_at 값 반영
    db.refresh(todo)
    return todo

# R : select
# select * from toodss where completed = 1 order by id desc
def select(completed:bool, db:Session, page:int, size:int):
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    offset = (page - 1) * size

    # 데이터
    todos = query.order_by(Todo.id.desc()).offset(offset).limit(size).all()
    # 전체개수
    total = query.count()
    # 화면에 보여줄 페이지 수
    total_pages = math.ceil(total / size)


    return {
        "items":todos,
        "total":total,
        "total_pages":total_pages,
        "page":page,
        "size":size,
        "completed":completed
    }

# U
def update(id:int,data:Todo,db:Session):
    # 수정할 대상 가져오기 
    todo = db.get(Todo, id)

    if todo is None:
        return None

    # 수정하기
    if data.title is not None:
        todo.title = data.title

    if data.completed is not None:
        todo.completed = data.completed

    if data.important is not None:
        todo.important = data.important


    db.commit()
    return id


# D
def delete(id:int, db:Session):
    # 수정할 대상 가져오기 
    todo = db.get(Todo, id)
    
    if todo is None:
        return None

    db.delete(todo)
    db.commit()
    return id