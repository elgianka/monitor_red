from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import ubicacion as ubicacion_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/ubicaciones", response_model=ubicacion_model.Ubicacion, tags=["Ubicaciones"])
def create_ubicacion(ubicacion: ubicacion_model.UbicacionCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_ubicacion = ubicacion_model.UbicacionDB(**ubicacion.dict())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@router.get("/ubicaciones", response_model=List[ubicacion_model.Ubicacion], tags=["Ubicaciones"])
def get_ubicaciones(db: Session = Depends(get_db)):
    ubicaciones = db.query(ubicacion_model.UbicacionDB).all()
    return ubicaciones

@router.get("/ubicaciones/{id_ubicacion}", response_model=ubicacion_model.Ubicacion, tags=["Ubicaciones"])
def get_ubicacion(id_ubicacion: int, db: Session = Depends(get_db)):
    ubicacion = db.query(ubicacion_model.UbicacionDB).filter(ubicacion_model.UbicacionDB.ID_UBICACION == id_ubicacion).first()
    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicacion not found")
    return ubicacion

@router.put("/ubicaciones/{id_ubicacion}", response_model=ubicacion_model.Ubicacion, tags=["Ubicaciones"])
def update_ubicacion(id_ubicacion: int, ubicacion: ubicacion_model.UbicacionCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_ubicacion = db.query(ubicacion_model.UbicacionDB).filter(ubicacion_model.UbicacionDB.ID_UBICACION == id_ubicacion).first()
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicacion not found")
    update_data = ubicacion.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ubicacion, key, value)
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@router.delete("/ubicaciones/{id_ubicacion}", status_code=204, tags=["Ubicaciones"])
def delete_ubicacion(id_ubicacion: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_ubicacion = db.query(ubicacion_model.UbicacionDB).filter(ubicacion_model.UbicacionDB.ID_UBICACION == id_ubicacion).first()
    if db_ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicacion not found")
    db.delete(db_ubicacion)
    db.commit()
    return
