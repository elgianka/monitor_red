from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import sede as sede_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/sedes", response_model=sede_model.Sede, tags=["Sedes"])
def create_sede(sede: sede_model.SedeCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea una nueva sede.
    """
    db_sede = sede_model.SedeDB(**sede.dict())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

@router.get("/sedes", response_model=List[sede_model.Sede], tags=["Sedes"])
def get_sedes(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las sedes.
    """
    sedes = db.query(sede_model.SedeDB).all()
    return sedes

@router.get("/sedes/{id_sede}", response_model=sede_model.Sede, tags=["Sedes"])
def get_sede(id_sede: int, db: Session = Depends(get_db)):
    """
    Obtiene una sede específica por su ID.
    """
    sede = db.query(sede_model.SedeDB).filter(sede_model.SedeDB.ID_SEDE == id_sede).first()
    if sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    return sede

@router.put("/sedes/{id_sede}", response_model=sede_model.Sede, tags=["Sedes"])
def update_sede(id_sede: int, sede: sede_model.SedeCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza una sede existente.
    """
    db_sede = db.query(sede_model.SedeDB).filter(sede_model.SedeDB.ID_SEDE == id_sede).first()
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    update_data = sede.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sede, key, value)
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

@router.delete("/sedes/{id_sede}", status_code=204, tags=["Sedes"])
def delete_sede(id_sede: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina una sede existente.
    """
    db_sede = db.query(sede_model.SedeDB).filter(sede_model.SedeDB.ID_SEDE == id_sede).first()
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    db.delete(db_sede)
    db.commit()
    return
