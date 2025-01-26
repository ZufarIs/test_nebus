from pydantic_settings import BaseSettings
from typing import Optional, Any

class Settings(BaseSettings):
    """
    Настройки приложения.
    
    Attributes:
        PROJECT_NAME (str): Название проекта
        VERSION (str): Версия API
        API_V1_STR (str): Префикс API v1
        DATABASE_TYPE (str): Тип базы данных ('sqlite' или 'postgresql')
        SQLITE_URL (str): URL для подключения к SQLite
        API_KEY (str): Ключ для аутентификации API
        POSTGRES_* (str/int): Настройки PostgreSQL
    """
    PROJECT_NAME: str = "Organization Directory API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_TYPE: str = "sqlite"
    SQLITE_URL: str = "sqlite:///./data/sql_app.db"
    API_KEY: str
    
    # POSTGRES_SERVER: str = "localhost"
    # POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "password"
    # POSTGRES_DB: str = "organization_directory"
    # POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует URL подключения к базе данных.
        
        Returns:
            str: URL для подключения к выбранной БД
        """
        if self.DATABASE_TYPE == "sqlite":
            return self.SQLITE_URL
        raise ValueError("Only sqlite is supported")

    class Config:
        env_file = ".env"

settings = Settings() 
