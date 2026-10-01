
from sqlalchemy import Identity, DateTime, String
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from repository.database import Base

# 테이블

class Todo(Base):

    __tablename__ = "todos"

    id:Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    title:Mapped[str] = mapped_column(String(255), nullable=False)
    completed:Mapped[bool] = mapped_column(default=False)
    important:Mapped[bool] = mapped_column(default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # onupdate=datetime.now : 수정 시 시간 자동으로
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Todo(id={self.id}, title={self.title})"
