from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Настройки приложения.
    
    Attributes:
        API_KEY (str): Ключ для аутентификации API
        POSTGRES_SERVER (str): Хост PostgreSQL
        POSTGRES_USER (str): Пользователь PostgreSQL
        POSTGRES_PASSWORD (str): Пароль PostgreSQL
        POSTGRES_DB (str): Имя базы данных
        POSTGRES_PORT (int): Порт PostgreSQL
        DATABASE_URL (str): URL подключения к базе данных
    """
    PROJECT_NAME: str = "Organization Directory API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    API_KEY: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    
    # Формирование DATABASE_URL
    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует URL подключения к базе данных.
        
        Returns:
            str: URL для подключения к PostgreSQL
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings() 
