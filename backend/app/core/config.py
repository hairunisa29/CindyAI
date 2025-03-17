from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CindyAI"
    
    # Security
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    
    # OpenAI
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 