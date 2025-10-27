from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import proceso as proceso_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/procesos", response_model=proceso_model.Proceso, tags=["Procesos"])
def create_proceso(proceso: proceso_model.ProcesoCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea un nuevo proceso.
    """
    db_proceso = proceso_model.ProcesoDB(**proceso.dict())
    db.add(db_proceso)
    db.commit()
    db.refresh(db_proceso)
    return db_proceso

@router.get("/procesos", response_model=List[proceso_model.Proceso], tags=["Procesos"])
def get_procesos(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los procesos.
    """
    procesos = db.query(proceso_model.ProcesoDB).all()
    return procesos

@router.get("/procesos/{id_proceso}", response_model=proceso_model.Proceso, tags=["Procesos"])
def get_proceso(id_proceso: int, db: Session = Depends(get_db)):
    """
    Obtiene un proceso específico por su ID.
    """
    proceso = db.query(proceso_model.ProcesoDB).filter(proceso_model.ProcesoDB.ID_PROCESO == id_proceso).first()
    if proceso is None:
        raise HTTPException(status_code=404, detail="Proceso not found")
    return proceso

@router.put("/procesos/{id_proceso}", response_model=proceso_model.Proceso, tags=["Procesos"])
def update_proceso(id_proceso: int, proceso: proceso_model.ProcesoCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza un proceso existente.
    """
    db_proceso = db.query(proceso_model.ProcesoDB).filter(proceso_model.ProcesoDB.ID_PROCESO == id_proceso).first()
    if db_proceso is None:
        raise HTTPException(status_code=404, detail="Proceso not found")
    update_data = proceso.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_proceso, key, value)
    db.add(db_proceso)
    db.commit()
    db.refresh(db_proceso)
    return db_proceso

@router.delete("/procesos/{id_proceso}", status_code=204, tags=["Procesos"])
def delete_proceso(id_proceso: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina un proceso existente.
    """
    db_proceso = db.query(proceso_model.ProcesoDB).filter(proceso_model.ProcesoDB.ID_PROCESO == id_proceso).first()
    if db_proceso is None:
        raise HTTPException(status_code=404, detail="Proceso not found")
    db.delete(db_proceso)
    db.commit()
    return
