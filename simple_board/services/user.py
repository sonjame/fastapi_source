from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.user import UserCreate, UserLogin,NameChange, PasswordChange, EmailChange
from repository.models.user import User
from exceptions.user import(
     UserAlreadyExistsExcepation, 
     UserNotFoundException, 
     InvalidPasswordException, 
     SamePasswordExcepation
)
from core.security import hash_password, verify_password

# CRUD 작업

# 이름 변경
def update_name(db: Session, data:NameChange, user_id:int):
    # 수정할 대상 찾기
    user = db.get(User, user_id)

    if user is None:
        raise UserNotFoundException

    # 수정하기
    user.name = data.name
    db.commit()
    db.refresh(user)
    return user

# 이메일 변경
def update_email(db: Session, data:EmailChange, user_id:int):
    # 수정할 대상 찾기
    user = db.get(User, user_id)

    if user is None:
        raise UserNotFoundException

    # 수정하기
    user.email = data.email
    db.commit()
    db.refresh(user)
    return user

# 비밀번호 변경
def update_password(db: Session, data:PasswordChange, user_id:int):
    # 수정할 대상 찾기
    user = db.get(User, user_id)

    if user is None:
        raise UserNotFoundException

    # current_password가 데이터베이스 비밀번호와 동일한가?
    if not verify_password(data.current_password, user.password):
        raise InvalidPasswordException

    # new_password가 데이터베이스 비밀번호와 동일한가?
    if verify_password(data.new_password, user.password):
        raise SamePasswordExcepation

    # 수정하기 - new_password 암호화 후 업데이트
    user.password = hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    return user


# 로그인
def authenticate(db:Session, data:UserLogin):
    # select * from board_users where id='입력한 이메일' and password = '12345'
    
    user = db.scalar(select(User).where(User.email == data.email))

    # 회원가입 정보가 없는 경우
    if user is None:
        raise UserNotFoundException

    # 비밀번호 검증 틀린 경우
    if not verify_password(data.password, user.password):
        raise InvalidPasswordException

    return user



# 회원가입
# 비밀번호 => 암호화
def register(db:Session, data:UserCreate):
    # 동일한 이메일로 가입된 정보가 있는가?
    # select * from board_users where email = '가입할려고 하는 이메일'
    exiting_user = db.scalar(select(User).where(User.email == data.email))

    if exiting_user:
        raise UserAlreadyExistsExcepation

    # 가입된 정보가 없을 때 회원가입
    user = User(email=data.email, password=hash_password(data.password), name=data.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

