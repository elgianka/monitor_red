from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import gerencia as gerencia_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/gerencias", response_model=gerencia_model.Gerencia, tags=["Gerencias"])
def create_gerencia(gerencia: gerencia_model.GerenciaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_gerencia = gerencia_model.GerenciaDB(NOM_GERENCIA=gerencia.NOM_GERENCIA)
    db.add(db_gerencia)
    db.commit()
    db.refresh(db_gerencia)
    return db_gerencia

@router.get("/gerencias", response_model=List[gerencia_model.Gerencia], tags=["Gerencias"])
def get_gerencias(db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    gerencias = db.query(gerencia_model.GerenciaDB).all()
    return gerencias

@router.get("/gerencias/{gerencia_id}", response_model=gerencia_model.Gerencia, tags=["Gerencias"])
def get_gerencia(gerencia_id: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    gerencia = db.query(gerencia_model.GerenciaDB).filter(gerencia_model.GerenciaDB.ID_GERENCIA == gerencia_id).first()
    if gerencia is None:
        raise HTTPException(status_code=404, detail="Gerencia not found")
    return gerencia

@router.put("/gerencias/{gerencia_id}", response_model=gerencia_model.Gerencia, tags=["Gerencias"])
def update_gerencia(gerencia_id: int, gerencia: gerencia_model.GerenciaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_gerencia = db.query(gerencia_model.GerenciaDB).filter(gerencia_model.GerenciaDB.ID_GERENCIA == gerencia_id).first()
    if db_gerencia is None:
        raise HTTPException(status_code=404, detail="Gerencia not found")
    db_gerencia.NOM_GERENCIA = gerencia.NOM_GERENCIA
    db.commit()
    db.refresh(db_gerencia)
    return db_gerencia

@router.delete("/gerencias/{gerencia_id}", status_code=204, tags=["Gerencias"])
def delete_gerencia(gerencia_id: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_gerencia = db.query(gerencia_model.GerenciaDB).filter(gerencia_model.GerenciaDB.ID_GERENCIA == gerencia_id).first()
    if db_gerencia is None:
        raise HTTPException(status_code=404, detail="Gerencia not found")
    db.delete(db_gerencia)
    db.commit()
    return
