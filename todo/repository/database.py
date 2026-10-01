# 데이터베이스 연결 설정
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.config import settings


database_url = URL.create(
    drivername="oracle+oracledb",
    username=settings.oracle_user,
    password=settings.oracle_password,
    host="localhost",
    port=1521,
    query={"service_name":"xe"}
)

engine = create_engine(database_url, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# SQLALchemy ORM 모델 부모 클래스
class Base(DeclarativeBase):
    pass

def init_db():
    from repository.models.todo import Todo
    # Base.metadata 에 등록된 테이블 생성(없을 때만 생성해줌)
    # 단점 : 컬럼 수정 반영 못해줌 => 다른 도구 필요
    Base.metadata.create_all(bind=engine)
    print("테이블 초기화 완료")

# API 요청 하나에서 사용할 DB session 만들어주고 요청이 완료되면 닫기
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
