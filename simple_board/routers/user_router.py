from fastapi import APIRouter, HTTPException, status
from services.user import (authenticate, register, update_name, update_email, update_password,)
from schemas.user import UserCreate, UserLogin, UserResponse, NameChange, PasswordChange, EmailChange
from sqlalchemy.orm import Session
from fastapi import Depends
from repository.database import get_db
from exceptions.user import UserAlreadyExistsExcepation, UserNotFoundException, InvalidPasswordException,  SamePasswordExcepation

auth_router = APIRouter(tags=["Users"])

# 회원가입 /auth + post
# 로그인 /auth/login + post
# 비밀번호수정 /auth/1/password + patch
# 이름수정 /auth/1/name + patch
# 이메일수정 /auth/1/email + patch

@auth_router.post(path="", response_model=dict)
async def post_signup(data:UserCreate, db:Session=Depends(get_db)) -> dict:
    try:
        user = register(data=data, db=db)
    except UserAlreadyExistsExcepation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="중복된 이메일이 존재합니다."
        )
    return {"message": "회원가입이 완료되었습니다.", "user_id":user.user_id}

@auth_router.post(path="/login", response_model=UserResponse)
async def post_signin(data:UserLogin, db:Session=Depends(get_db)) -> UserResponse:
    try:
        user = authenticate(data=data, db=db)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="아이디나 비밀번호를 확인해주세요",)
    except InvalidPasswordException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="아이디나 비밀번호를 확인해주세요",)

    return user

@auth_router.patch(path="/{user_id}/name", response_model=dict)
async def patch_name(user_id:int, data:NameChange, db:Session=Depends(get_db)):

    try:
        update_name(db=db, user_id=user_id, data=data)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 사용자입니다")


    return {"message": "이름이 변경되었습니다"}

@auth_router.patch(path="/{user_id}/email", response_model=dict)
async def patch_email(user_id:int ,data:EmailChange, db:Session=Depends(get_db)):
    try:
        update_email(db=db, user_id=user_id, data=data)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 사용자입니다")

    return {"message": "이메일 변경되었습니다"}

@auth_router.patch(path="/{user_id}/password", response_model=dict)
async def patch_password(user_id:int, data:PasswordChange, db:Session=Depends(get_db)):
    try:
        update_password(db=db, user_id=user_id ,data=data)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 사용자입니다")  
    except InvalidPasswordException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="기존 비밀번호를 확인해 주세요")  
    except SamePasswordExcepation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="기존 비밀번호와 다른 비밀번호를 사용해 주세요")  
    
    return {"message": "비밀번호 변경되었습니다"}
