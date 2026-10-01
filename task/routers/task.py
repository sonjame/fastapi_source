from fastapi import APIRouter, HTTPException, status
from schemas.task import TaskCreate, TaskPageResponse, TaskUpdate
from sqlalchemy.orm import Session
from repository.database import get_db
from fastapi import Depends
from services.task import create, select, update, delete
from exceptions.task import TaskNotFoundException

task_router = APIRouter(tags=["Tasks"])

@task_router.post("", response_model=dict)
async def post_tasks(data:TaskCreate, db: Session = Depends(get_db)):
   task = create(data, db=db)

   return {"message":f"Task {task.id} 삽입 성공"}

# 전체조회, 수정(put, patch), 삭제, 추가

@task_router.get("", response_model=TaskPageResponse)
async def get_tasks(db: Session = Depends(get_db), page: int = 1, size: int = 10):
    tasks = select(page=page, size=size, db=db)
    return tasks

# client 수정 done
# client 수정 text
@task_router.put("/{id}", response_model=dict)
async def put_tasks(id:int, update_task:TaskUpdate, db: Session = Depends(get_db)):

    try:
        task = update(db=db, data=update_task, id=id)
    except TaskNotFoundException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="해당하는 task 가 없습니다"
        )

    return {"message":f"Task {task.id} 수정 완료"}

@task_router.delete("/{id}", response_model=dict)
async def delete_tasks(id:int,  db: Session = Depends(get_db)):
    try:
        id = delete(id=id, db=db)
    except TaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="해당하는 task 가 없습니다")    

    return {"message":f"Task {id} 수정 완료"}
