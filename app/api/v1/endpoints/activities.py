from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.schemas.activity import Activity, ActivityCreate
from app.models.activity import Activity as ActivityModel
from app.crud.activity import get_activities, get_activity as crud_get_activity

router = APIRouter()

@router.get("/", response_model=List[Activity])
def read_activities(db: Session = Depends(get_db)):
    """
    Получить дерево видов деятельности.
    """
    return get_activities(db)

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Получить вид деятельности по ID.
    """
    db_activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Преобразуем модель в схему с явной инициализацией children
    return Activity(
        id=db_activity.id,
        name=db_activity.name,
        level=db_activity.level,
        parent_id=db_activity.parent_id,
        children=[Activity(
            id=child.id,
            name=child.name,
            level=child.level,
            parent_id=child.parent_id,
            children=[]
        ) for child in db_activity.children] if db_activity.children else []
    )

@router.post("/", response_model=Activity)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Создать новый вид деятельности.
    
    Args:
        activity: Данные для создания вида деятельности
        db: Сессия базы данных
        api_key: API ключ для аутентификации
    
    Returns:
        Activity: Созданный вид деятельности
        
    Raises:
        HTTPException: Если превышен максимальный уровень вложенности
    """
    # Проверка уровня вложенности
    if activity.parent_id:
        parent = db.query(ActivityModel).filter(ActivityModel.id == activity.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent activity not found")
        if parent.level >= 3:
            raise HTTPException(
                status_code=400,
                detail="Maximum nesting level (3) exceeded"
            )
        activity.level = parent.level + 1
    else:
        activity.level = 1  # Корневой уровень
        activity.parent_id = None  # Убираем parent_id=0
    
    # Создаем новую активность
    db_activity = ActivityModel(
        name=activity.name,
        level=activity.level,
        parent_id=activity.parent_id
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return Activity(
        id=db_activity.id,
        name=db_activity.name,
        level=db_activity.level,
        parent_id=db_activity.parent_id,
        children=[]  # Инициализируем пустым списком
    ) 
