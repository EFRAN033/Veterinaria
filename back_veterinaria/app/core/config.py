from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Union
from pydantic import field_validator

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    # Email
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",")]
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                try:
                    # Try to fix single quotes common mistake
                    return json.loads(v.replace("'", '"'))
                except:
                    # Fallback to simple string if JSON fails
                    return [i.strip() for i in v.split(",")]
        return v

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
