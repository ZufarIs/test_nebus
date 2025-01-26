from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.activity import Activity
from geopy.distance import geodesic
from app.crud.activity import get_all_child_activity_ids  # Импортируем из activity.py

def get_organizations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    activity_id: Optional[int] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: Optional[float] = None
) -> List[Organization]:
    """Получить список организаций с фильтрацией."""
    query = db.query(Organization)

    if activity_id:
        activity_ids = get_all_child_activity_ids(db, activity_id)  # Используем импортированную функцию
        query = query.filter(
            Organization.activities.any(Activity.id.in_(activity_ids))
        )

    organizations = query.offset(skip).limit(limit).all()

    if lat and lon and radius:
        filtered_orgs = []
        point1 = (lat, lon)
        for org in organizations:
            point2 = (org.building.latitude, org.building.longitude)
            distance = geodesic(point1, point2).kilometers
            if distance <= radius:
                filtered_orgs.append(org)
        return filtered_orgs

    return organizations

def get_organization(db: Session, org_id: int) -> Optional[Organization]:
    """
    Получить организацию по ID.
    """
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_organizations_by_building(
    db: Session,
    building_id: int
) -> List[Organization]:
    """
    Получить список организаций в конкретном здании.
    
    Args:
        db: Сессия базы данных
        building_id: ID здания
        
    Returns:
        List[Organization]: Список организаций в здании
    """
    return db.query(Organization).filter(
        Organization.building_id == building_id
    ).all() 
