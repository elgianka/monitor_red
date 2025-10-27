from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import modelo as modelo_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/modelos", response_model=modelo_model.Modelo, tags=["Modelos"])
def create_modelo(modelo: modelo_model.ModeloCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea un nuevo modelo.
    """
    db_modelo = modelo_model.ModeloDB(**modelo.dict())
    db.add(db_modelo)
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

@router.get("/modelos", response_model=List[modelo_model.Modelo], tags=["Modelos"])
def get_modelos(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los modelos.
    """
    modelos = db.query(modelo_model.ModeloDB).all()
    return modelos

@router.get("/modelos/{id_modelo}", response_model=modelo_model.Modelo, tags=["Modelos"])
def get_modelo(id_modelo: int, db: Session = Depends(get_db)):
    """
    Obtiene un modelo específico por su ID.
    """
    modelo = db.query(modelo_model.ModeloDB).filter(modelo_model.ModeloDB.ID_MODELO == id_modelo).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo not found")
    return modelo

@router.put("/modelos/{id_modelo}", response_model=modelo_model.Modelo, tags=["Modelos"])
def update_modelo(id_modelo: int, modelo: modelo_model.ModeloCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza un modelo existente.
    """
    db_modelo = db.query(modelo_model.ModeloDB).filter(modelo_model.ModeloDB.ID_MODELO == id_modelo).first()
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo not found")
    update_data = modelo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_modelo, key, value)
    db.add(db_modelo)
    db.commit()
    db.refresh(db_modelo)
    return db_modelo

@router.delete("/modelos/{id_modelo}", status_code=204, tags=["Modelos"])
def delete_modelo(id_modelo: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina un modelo existente.
    """
    db_modelo = db.query(modelo_model.ModeloDB).filter(modelo_model.ModeloDB.ID_MODELO == id_modelo).first()
    if db_modelo is None:
        raise HTTPException(status_code=404, detail="Modelo not found")
    db.delete(db_modelo)
    db.commit()
    return
