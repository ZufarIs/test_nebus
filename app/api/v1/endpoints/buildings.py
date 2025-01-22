from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.schemas.building import Building, BuildingCreate
from app.models.building import Building as BuildingModel

router = APIRouter()

@router.get("/", response_model=List[Building])
async def get_buildings(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    return db.query(BuildingModel).all()

@router.get("/{building_id}", response_model=Building)
async def get_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
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
    db_building = BuildingModel(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building 
