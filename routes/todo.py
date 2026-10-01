# /todos/ 로 들어오는 요청 처리

# /todos/ + GET: 전체조회
# /todos/1 + GET: 특정 todo 조회
# /todos/ + 삽입데이터 + POST: 특정 todo 삽입
# /todos/1 + 수정데이터 + PUT: 특정 todo 수정
# /todos/1 + DELETE: 특정 todo 삭제


from models.model import TodoItem
from fastapi import APIRouter, HTTPException, status

todo_router = APIRouter(prefix="/todos")


todos = [
  {
    "id": 1,
    "title": "react 기초 알아보기",
    "completed": True,
    "important": True
  },
  {
    "id": 2,
    "title": "컴포넌트 스타일링해 보기",
    "completed": True,
    "important": False
  },
  {
    "id": 3,
    "title": "일정관리 앱 만들어보기",
    "completed": False,
    "important": False
  },
]

# 딕셔너리의 키를 함수/클래스 매개 변수 이름으로 풀어서 전달
# [ TodoItem(), TodoItem(), ...]
todo_items = [TodoItem(**todo) for todo in todos]

# 전체 조회
@todo_router.get("/")
async def get_todos():
    return {"todos":todo_items}
    

# 특정 조회 : 먼저 매핑된것이 적용됨 
@todo_router.get("/{id}")
async def get_todo(id:int):

    for todo in todo_items:
        if todo.id == id:
            return {"todo":todo}

    return {"todo":"todo를 찾을수 없습니다"}

# /todos/ + 삽입데이터 + POST: 특정 todo 삽입
@todo_router.post("/")
async def post_todo(todo:TodoItem):
    todo_items.append(todo)
    return {"todos":todo_items}

# 경로매개변수 : /todos/1
# 쿼리매개변수 : /todos/?id=1
@todo_router.get("/get")
async def get_query_todo(id:int):

    for todo in todo_items:
        if todo.id == id:
            return {"todo":todo}

    return {"todo":"todo를 찾을수 없습니다"}

# /todos/1 + 수정데이터 + PUT: 특정 todo 수정
@todo_router.put("/{todo_id}")
async def put_todo(todo_id:int,update_todo:TodoItem) -> dict:
    for todo in todo_items:
        if todo.id == todo_id:
            todo.title = update_todo.title
            todo.completed = update_todo.completed
            todo.important = update_todo.important
            return {"todo":todo}
    
    return {"todo":"todo를 찾을 수 없습니다."}

# /todos/1 + DELETE: 특정 todo 삭제
@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id:int) -> dict:
    for todo in todo_items:
        if todo.id == todo_id:
            todo_items.remove(todo)
            return{"todo_items":todo_items}
    return {"todo":"todo를 찾을 수 없습니다."}