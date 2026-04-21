from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    PORT: int = 8000
    HOST: str = "0.0.0.0"

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""

    # CORS — URL del frontend principal
    FRONTEND_URL: str = "http://localhost:5173"
    # CORS — Orígenes adicionales separados por coma
    # Ejemplo: https://veterinaria-k6f4.onrender.com,https://otro.com
    BACKEND_CORS_ORIGINS: str = ""

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL

    @property
    def cors_origins(self) -> List[str]:
        """Retorna todos los orígenes CORS permitidos como lista."""
        origins = [self.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"]
        if self.BACKEND_CORS_ORIGINS:
            extra = [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]
            origins.extend(extra)
        return list(dict.fromkeys(origins))  # Eliminar duplicados preservando orden


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
