from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.board_router import board_router
from routers.user_router import auth_router
from routers.comment_router import comment_router
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan, title="Board & User Project", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # 어떤 출처의 요청을 허용할 것인가?
    allow_credentials=True, # 쿠키나 인증정보를 포함한 요청을 허용할 것인가?
    allow_methods=["*"],  # 어떤 메소드를 허용할 것인가? (post, get, put, patch, delete)
    allow_headers=["*"]   # 요청에서 사용할 수 있는 헤더정보
)

# router 설정 - 개별 라우터 생성 후 포함
app.include_router(board_router, prefix="/boards")
app.include_router(auth_router, prefix="/auth")
app.include_router(comment_router, prefix="/comments")

