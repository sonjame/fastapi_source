from repository.database import Base
from sqlalchemy import Identity, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

# user_id : pk
# email : unique
# password
# name
# 가입일


class User(Base):

    __tablename__ = "board_users"

    user_id:Mapped[int] = mapped_column(
        Identity(start=1, increment=1), primary_key=True
    )
    email:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password:Mapped[str] = mapped_column(String(100), nullable=False)
    name:Mapped[str] = mapped_column(String(50), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    # user.boards.
    boards:Mapped[list["Board"]] = relationship(back_populates="user")
    # user.comments
    comments:Mapped[list["Comment"]] = relationship(back_populates="user")

