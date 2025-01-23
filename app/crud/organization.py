from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.activity import Activity
from geopy.distance import geodesic

def get_all_child_activity_ids(db: Session, activity_id: int) -> List[int]:
    """Рекурсивно получает все дочерние ID для заданного activity_id."""
    activity_ids = [activity_id]
    stack = [activity_id]
    
    while stack:
        current_id = stack.pop()
        current = db.query(Activity).get(current_id)
        if current:
            children = current.children or []
            child_ids = [child.id for child in children]
            activity_ids.extend(child_ids)
            stack.extend(child_ids)
    
    return activity_ids

def get_organizations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    activity_id: Optional[int] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: Optional[float] = None
) -> List[Organization]:
    """
    Получить список организаций с фильтрацией.
    """
    query = db.query(Organization)

    if activity_id:
        # Получаем все ID активностей, включая дочерние
        activity_ids = get_all_child_activity_ids(db, activity_id)
        query = query.filter(
            Organization.activities.any(Activity.id.in_(activity_ids))
        )

    # Сначала получаем базовый список организаций
    organizations = query.offset(skip).limit(limit).all()

    # Если указаны координаты и радиус, фильтруем по расстоянию
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
