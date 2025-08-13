from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI SQLAlchemy Project"
    API_V1_STR: str = "/api/v1"
    PROJECT_DESCRIPTION: str = "A FastAPI project with SQLAlchemy"
    VERSION: str = "1.0.0"
    
    # Database
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"
        env_file_encoding = 'utf-8'

settings = Settings()