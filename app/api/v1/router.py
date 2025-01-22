from fastapi import APIRouter
from app.api.v1.endpoints import organizations, buildings, activities

def get_api_router() -> APIRouter:
    """
    Создает и настраивает основной API роутер.
    
    Returns:
        APIRouter: Настроенный роутер с подключенными эндпоинтами
    """
    api_router = APIRouter()
    api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
    api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
    api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
    return api_router 
