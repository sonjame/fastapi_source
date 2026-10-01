from sqlalchemy.orm import Session
from repository.models.task import Task
from schemas.task import  TaskCreate, TaskUpdate
from exceptions.task import TaskNotFoundException
import math

# CRUD 작업

#c
def create(data: TaskCreate, db: Session):
    task = Task(text=data.text, done=data.done)
    db.add(task)
    db.commit()

    db.refresh(task)
    return task

def select(page:int, size:int, db: Session):

    query = db.query(Task)

    offset = (page - 1) * size
    total = query.count()
    # order by
    tasks = query.order_by(Task.id.desc()).offset(offset).limit(size).all()
    total_pages = math.ceil(total / size)

    return{
        "items":tasks,
        "total":total,
        "total_pages":total_pages,
        "page":page,
        "size":size,
    }

def update(db: Session, data:TaskUpdate, id:int):
    # 수정할 대상 가져오기
    # get() : pk 기준으로 하나 가져올때 사용
    task = db.get(Task, id)

    if task is None:
        raise TaskNotFoundException

    if data.text is not None:
        task.text = data.text

    if data.done is not None:
        task.done = data.done

    db.commit()
    return task


def delete(db: Session, id:int):
    task = db.get(Task, id)

    if task is None:
        raise TaskNotFoundException

    db.delete(task)
    db.commit()
    return id
    
