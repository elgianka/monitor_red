from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import estado as estado_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/estados", response_model=estado_model.Estado, tags=["Estados"])
def create_estado(estado: estado_model.EstadoCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea un nuevo estado.
    """
    db_estado = estado_model.EstadoDB(**estado.dict())
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.get("/estados", response_model=List[estado_model.Estado], tags=["Estados"])
def get_estados(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los estados.
    """
    estados = db.query(estado_model.EstadoDB).all()
    return estados

@router.get("/estados/{id_estado}", response_model=estado_model.Estado, tags=["Estados"])
def get_estado(id_estado: int, db: Session = Depends(get_db)):
    """
    Obtiene un estado específico por su ID.
    """
    estado = db.query(estado_model.EstadoDB).filter(estado_model.EstadoDB.ID_ESTADO == id_estado).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado not found")
    return estado

@router.put("/estados/{id_estado}", response_model=estado_model.Estado, tags=["Estados"])
def update_estado(id_estado: int, estado: estado_model.EstadoCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza un estado existente.
    """
    db_estado = db.query(estado_model.EstadoDB).filter(estado_model.EstadoDB.ID_ESTADO == id_estado).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado not found")
    update_data = estado.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_estado, key, value)
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.delete("/estados/{id_estado}", status_code=204, tags=["Estados"])
def delete_estado(id_estado: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina un estado existente.
    """
    db_estado = db.query(estado_model.EstadoDB).filter(estado_model.EstadoDB.ID_ESTADO == id_estado).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado not found")
    db.delete(db_estado)
    db.commit()
    return
