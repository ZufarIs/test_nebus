from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import get_api_router
from pydantic import BaseModel
from typing import List, Optional

def create_application() -> FastAPI:
    """Создает и настраивает экземпляр FastAPI приложения."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc"
    )
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    api_router = get_api_router()
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

app = create_application()

"""
Настройка CORS middleware для обработки кросс-доменных запросов.
Внимание: в продакшене следует указать конкретные разрешенные домены вместо "*".
"""

class ActivityCreate(BaseModel):
    name: str
    level: int
    parent_id: Optional[int] = None
    children: List = []

    class Config:
        from_attributes = True 
