from repository.database import Base
from sqlalchemy import Identity, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

# id:pk
# 내용, 작성자, 작성일, 수정일, board_id 
class Comment(Base):

    __tablename__ = "comments"

    comment_id:Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    body:Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id:Mapped[int] = mapped_column(
        ForeignKey("board_users.user_id"), nullable=False
    )
    board_id:Mapped[int] = mapped_column( ForeignKey("boards.id"), nullable=False)
    # 컬럼의 개념 아님(파이썬 객체간 연결)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # comment.user.name~~
    user: Mapped["User"] = relationship(back_populates="comments")
    # comment.board.~~
    board: Mapped["Board"] = relationship(back_populates="comments")
