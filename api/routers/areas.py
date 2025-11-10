from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import area as area_model, user as user_model, gerencia as gerencia_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/areas", response_model=area_model.Area, tags=["Areas"])
def create_area(area: area_model.AreaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_gerencia = db.query(gerencia_model.GerenciaDB).filter(gerencia_model.GerenciaDB.ID_GERENCIA == area.ID_GERENCIA).first()
    if not db_gerencia:
        raise HTTPException(status_code=404, detail="Gerencia not found")

    db_area = area_model.AreaDB(NOM_AREA=area.NOM_AREA, ID_GERENCIA=area.ID_GERENCIA)
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

@router.get("/areas", response_model=List[area_model.Area], tags=["Areas"])
def get_areas(db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    areas = db.query(area_model.AreaDB).all()
    return areas

@router.get("/areas/{area_id}", response_model=area_model.Area, tags=["Areas"])
def get_area(area_id: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    area = db.query(area_model.AreaDB).filter(area_model.AreaDB.ID_AREA == area_id).first()
    if area is None:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

@router.put("/areas/{area_id}", response_model=area_model.Area, tags=["Areas"])
def update_area(area_id: int, area: area_model.AreaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_area = db.query(area_model.AreaDB).filter(area_model.AreaDB.ID_AREA == area_id).first()
    if db_area is None:
        raise HTTPException(status_code=404, detail="Area not found")
    
    db_gerencia = db.query(gerencia_model.GerenciaDB).filter(gerencia_model.GerenciaDB.ID_GERENCIA == area.ID_GERENCIA).first()
    if not db_gerencia:
        raise HTTPException(status_code=404, detail="Gerencia not found")

    db_area.NOM_AREA = area.NOM_AREA
    db_area.ID_GERENCIA = area.ID_GERENCIA
    db.commit()
    db.refresh(db_area)
    return db_area

@router.delete("/areas/{area_id}", status_code=204, tags=["Areas"])
def delete_area(area_id: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_area = db.query(area_model.AreaDB).filter(area_model.AreaDB.ID_AREA == area_id).first()
    if db_area is None:
        raise HTTPException(status_code=404, detail="Area not found")
    db.delete(db_area)
    db.commit()
    return
