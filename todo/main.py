from fastapi import FastAPI
from routes.todo import todo_router
from fastapi.middleware.cors import CORSMiddleware
from core.lifespan import lifespan

app = FastAPI(title="Todo Project", version="1.0", lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # 어떤 출처의 요청을 허용할 것인가?
    allow_credentials=True, # 쿠키나 인증정보를 포함한 요청을 허용할 것인가?
    allow_methods=["*"], # 어떤 메소드를 허용할 것인가? (post, get, put, patch, delete)
    allow_headers=["*"]  # 요청에서 사용할 수 있는 헤더정보
)



app.include_router(todo_router)



# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# http://127.0.0.1:8000/todos/1
# @app.get("/todos/{id}")
# def read_todo(id: int):
#     return {"id": id}