from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

def create_application() -> FastAPI:
    """
    Создает и настраивает экземпляр FastAPI приложения.
    
    Returns:
        FastAPI: Настроенное приложение
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    api_router = get_api_router()
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

app = create_application()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
Настройка CORS middleware для обработки кросс-доменных запросов.
Внимание: в продакшене следует указать конкретные разрешенные домены вместо "*".
"""

# Подключение роутера API
app.include_router(api_router, prefix=settings.API_V1_STR) 
