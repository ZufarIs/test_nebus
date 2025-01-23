from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.security import get_api_key
from app.db.session import get_db
from app.schemas.organization import Organization, OrganizationDetail
from app.models.organization import Organization as OrganizationModel
from app.models.building import Building
from app.models.activity import Activity as ActivityModel
from geopy.distance import geodesic

router = APIRouter()

def get_all_child_activity_ids(db: Session, activity_id: int) -> List[int]:
    """Рекурсивно получает все дочерние ID для заданного activity_id."""
    activity_ids = [activity_id]
    stack = [activity_id]
    
    while stack:
        current_id = stack.pop()
        current = db.query(ActivityModel).get(current_id)
        if current:
            # Исправление: проверяем наличие children
            children = current.children or []
            child_ids = [child.id for child in children]
            activity_ids.extend(child_ids)
            stack.extend(child_ids)
    
    return activity_ids

@router.get("/", response_model=List[OrganizationDetail])
async def get_organizations(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key),
    building_id: int = None,
    activity_id: int = None,
    lat: float = None,
    lon: float = None,
    radius: float = None,
    name: str = None
):
    """
    Получить список организаций с возможностью фильтрации.
    
    Args:
        db: Сессия базы данных
        api_key: API ключ для аутентификации
        building_id: Фильтр по ID здания
        activity_id: Фильтр по ID вида деятельности
        lat: Широта для поиска по радиусу
        lon: Долгота для поиска по радиусу
        radius: Радиус поиска в километрах
    
    Returns:
        List[OrganizationDetail]: Список организаций
    """
    query = db.query(OrganizationModel)

    if building_id:
        query = query.filter(OrganizationModel.building_id == building_id)
    
    if activity_id:
        activity_ids = get_all_child_activity_ids(db, activity_id)
        query = query.filter(
            OrganizationModel.activities.any(ActivityModel.id.in_(activity_ids))
        )

    if lat and lon and radius:
        # Фильтрация по радиусу
        organizations = query.all()
        filtered_orgs = []
        point1 = (lat, lon)
        
        for org in organizations:
            point2 = (org.building.latitude, org.building.longitude)
            distance = geodesic(point1, point2).kilometers
            if distance <= radius:
                filtered_orgs.append(org)
        
        return filtered_orgs

    if name:
        # Используем case-insensitive поиск, совместимый с обоими SQLite и PostgreSQL
        query = query.filter(func.lower(OrganizationModel.name).like(f"%{name.lower()}%"))

    return query.all()

@router.get("/{org_id}", response_model=Organization)
async def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Получить информацию о конкретной организации.
    
    Args:
        org_id: ID организации
        db: Сессия базы данных
        api_key: API ключ для аутентификации
    
    Returns:
        Organization: Информация об организации
        
    Raises:
        HTTPException: Если организация не найдена
    """
    org = db.query(OrganizationModel).filter(OrganizationModel.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org 
