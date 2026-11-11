from repository.database import Base
from sqlalchemy import Identity, DateTime, Integer, String, ForeignKey, UniqueConstraint
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
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    # 조회수 컬럼
    views:Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # 컬럽의 개념 아님(파이썬 객체간 연결)
    # board.user.email
    user: Mapped["User"] = relationship(back_populates="boards")

    # board.comments.count()
    comments:Mapped[list["Comment"]] = relationship(back_populates="boards")

class Board_Views(Base):
    __tablename__ = "board_views"

    # unique 제약조건 37번글을, 1번 user가 읽음
    __table_args__ = (
        UniqueConstraint("board_id", "user_id", name="uq_board_view_user"),
    )

    id:Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    user_id:Mapped[int] = mapped_column(
        ForeignKey("board_users.user_id"), nullable=False
    )
    board_id: Mapped[int] = mapped_column( ForeignKey("boards.id"), nullable=False)
    viewed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
