# 프로젝트 환경설정 파일
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    oracle_user:str = Field(alias="ORACLE_USER")
    oracle_password:str = Field(alias="ORACLE_PASSWORD")

settings = Settings()
