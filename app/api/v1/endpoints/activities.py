from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.schemas.activity import Activity, ActivityCreate
from app.models.activity import Activity as ActivityModel

router = APIRouter()

@router.get("/", response_model=List[Activity])
async def get_activities(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    return db.query(ActivityModel).filter(ActivityModel.parent_id.is_(None)).all()

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("/", response_model=Activity)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
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
    
    db_activity = ActivityModel(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity 
