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
from app.crud.organization import get_organizations, get_organization

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
def read_organizations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    activity_id: Optional[int] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: Optional[float] = None
):
    """
    Получить список организаций с фильтрацией.
    """
    organizations = get_organizations(
        db, 
        skip=skip, 
        limit=limit,
        activity_id=activity_id,
        lat=lat,
        lon=lon,
        radius=radius
    )
    return organizations

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
