from repository.database import Base
from sqlalchemy import Identity, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


# 데이터베이스 테이브로가 연동
class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)



    

