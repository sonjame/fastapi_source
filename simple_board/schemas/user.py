# 프론트엔드에서 IN/OUT 데이터 검증
from pydantic import BaseModel, EmailStr, Field, ConfigDict, AfterValidator
from typing import Annotated
import re 

SPECIAL_CHARS = "@!$*-"


def validate_password_strength(v:str)->str:
    if not re.search(r"[A-Z]",v):
        raise ValueError('대문자를 1자 이상 포함해야 합니다.')
    if not re.search(r"[a-z]",v):
        raise ValueError('소문자를 1자 이상 포함해야 합니다.')
    if not re.search(r"\d",v):
        raise ValueError('숫자를 1자 이상 포함해야 합니다.')
    if not any(c in SPECIAL_CHARS for c in v):
        raise ValueError(f'특수문자{SPECIAL_CHARS}를 1자 이상 포함해야 합니다.')
    return v



Password = Annotated[
    str, Field(min_length=8, max_length=64), AfterValidator(validate_password_strength)
]

# 회원가입 - 비밀번호 규칙 적용(대문자,소문자,숫자,특수문자(@!$*-))
class UserCreate(BaseModel):
    email:EmailStr
    password: Password
    name:str=Field(min_length=1, max_length=30)

# 로그인
class UserLogin(BaseModel):
    email:str
    password: str

# 비밀번호 변경
class PasswordChange(BaseModel):
    current_password:str
    new_password: Password

# 이름 변경
class NameChange(BaseModel):
    name:str = Field(min_length=1, max_length=30)

# 이메일 변경
class EmailChange(BaseModel):
    email:EmailStr

class UserResponse(BaseModel):
    user_id:int
    email: EmailStr
    name: str
