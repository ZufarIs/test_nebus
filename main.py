import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import get_api_router
from app.db.session import engine
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal

def init_database():
    """
    Инициализация базы данных при первом запуске.
    Создает таблицы и заполняет их тестовыми данными, если БД не существует.
    """
    db_path = "sql_app.db"
    is_first_run = not os.path.exists(db_path)
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Если это первый запуск, инициализируем тестовые данные
    if is_first_run:
        print("Инициализация базы данных...")
        db = SessionLocal()
        try:
            init_db(db)
            print("База данных успешно инициализирована.")
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
        finally:
            db.close()

def create_application() -> FastAPI:
    """
    Создает и настраивает экземпляр FastAPI приложения.
    
    Returns:
        FastAPI: Настроенное приложение
    """
    # Инициализируем БД при необходимости
    init_database()
    
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Настройка CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене нужно указать конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Подключение роутера API
    api_router = get_api_router()
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

app = create_application()

"""
Настройка CORS middleware для обработки кросс-доменных запросов.
Внимание: в продакшене следует указать конкретные разрешенные домены вместо "*".
"""

# Подключение роутера API
api_router = get_api_router()
app.include_router(api_router, prefix=settings.API_V1_STR) 
