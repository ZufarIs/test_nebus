from fastapi import APIRouter
from app.api.v1.endpoints import organizations, buildings, activities

api_router = APIRouter()

api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["organizations"]
)

api_router.include_router(
    buildings.router,
    prefix="/buildings",
    tags=["buildings"]
)

api_router.include_router(
    activities.router,
    prefix="/activities",
    tags=["activities"]
) 
