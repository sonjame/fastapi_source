from core.config import settings
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from exceptions.user import UserCredentialsExcepation

def verity_access_token(token:str) -> dict:
    """
    jwt 토큰 검증 및 디코딩 후 문자열 반환
    """

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        return payload
    except InvalidTokenError:
        raise UserCredentialsExcepation





def create_access_token(data:dict, expires_delta:int=3600) -> str:
    """
    jwt 토큰 생성
    data : 토큰에 포함한 데이터(ex: 사용자 정보)
    expire_delta : 토큰 만료시간(초 단위, 기본값 1시간)
    return : 생성된 JWT 토큰 문자열
    """
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encode_jwt

