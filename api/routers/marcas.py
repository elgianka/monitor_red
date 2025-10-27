from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import marca as marca_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/marcas", response_model=marca_model.Marca, tags=["Marcas"])
def create_marca(marca: marca_model.MarcaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea una nueva marca.
    """
    db_marca = marca_model.MarcaDB(**marca.dict())
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.get("/marcas", response_model=List[marca_model.Marca], tags=["Marcas"])
def get_marcas(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las marcas.
    """
    marcas = db.query(marca_model.MarcaDB).all()
    return marcas

@router.get("/marcas/{id_marca}", response_model=marca_model.Marca, tags=["Marcas"])
def get_marca(id_marca: int, db: Session = Depends(get_db)):
    """
    Obtiene una marca específica por su ID.
    """
    marca = db.query(marca_model.MarcaDB).filter(marca_model.MarcaDB.ID_MARCA == id_marca).first()
    if marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return marca

@router.put("/marcas/{id_marca}", response_model=marca_model.Marca, tags=["Marcas"])
def update_marca(id_marca: int, marca: marca_model.MarcaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza una marca existente.
    """
    db_marca = db.query(marca_model.MarcaDB).filter(marca_model.MarcaDB.ID_MARCA == id_marca).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    update_data = marca.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_marca, key, value)
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.delete("/marcas/{id_marca}", status_code=204, tags=["Marcas"])
def delete_marca(id_marca: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina una marca existente.
    """
    db_marca = db.query(marca_model.MarcaDB).filter(marca_model.MarcaDB.ID_MARCA == id_marca).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    db.delete(db_marca)
    db.commit()
    return
