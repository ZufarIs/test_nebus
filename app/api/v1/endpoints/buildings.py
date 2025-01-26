from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.schemas.building import Building, BuildingCreate
from app.models.building import Building as BuildingModel
from app.schemas.organization import OrganizationDetail
from app.crud.organization import get_organizations_by_building

router = APIRouter()

@router.get("/", response_model=List[Building])
async def get_buildings(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Получить список всех зданий.
    
    Args:
        db: Сессия базы данных
        api_key: API ключ для аутентификации
    
    Returns:
        List[Building]: Список зданий
    """
    return db.query(BuildingModel).all()

@router.get("/{building_id}", response_model=Building)
async def get_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Получить информацию о конкретном здании.
    
    Args:
        building_id: ID здания
        db: Сессия базы данных
        api_key: API ключ для аутентификации
    
    Returns:
        Building: Информация о здании
        
    Raises:
        HTTPException: Если здание не найдено
    """
    building = db.query(BuildingModel).filter(BuildingModel.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.post("/", response_model=Building)
async def create_building(
    building: BuildingCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Создать новое здание.
    
    Args:
        building: Данные для создания здания
        db: Сессия базы данных
        api_key: API ключ для аутентификации
    
    Returns:
        Building: Созданное здание
    """
    db_building = BuildingModel(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building 

@router.get("/{building_id}/organizations", response_model=List[OrganizationDetail])
def read_building_organizations(
    building_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить список всех организаций в конкретном здании.
    
    Args:
        building_id: ID здания
        db: Сессия базы данных
        
    Returns:
        List[OrganizationDetail]: Список организаций в здании
        
    Raises:
        HTTPException: Если здание не найдено
    """
    # Проверяем существование здания
    building = db.query(BuildingModel).filter(BuildingModel.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
        
    return get_organizations_by_building(db, building_id)
