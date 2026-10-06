from repository.database import Base
from sqlalchemy import Identity, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

# id:pk
# 제목, 내용, 작성자, 작성일, 수정일
class Board(Base):

    __tablename__ = "boards"

    id:Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    contents:Mapped[str] = mapped_column(String(2000), nullable=False)
    user_id:Mapped[int] = mapped_column(
        ForeignKey("board_users.user_id"), nullable=False
    )
    # 컬럼의 개념 아님(파이썬 객체간 연결)
    # board.user.email
    user:Mapped["User"] = relationship(back_populates="boards")
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # 컬럽의 개념 아님(파이썬 객체간 연결)
    # board.user.email
    user: Mapped["User"] = relationship(back_populates="boards")

    # board.comments.count()
    comments:Mapped[list["Comment"]] = relationship(back_populates="board")
