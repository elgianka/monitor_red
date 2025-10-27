from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import categoria as categoria_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/categorias", response_model=categoria_model.Categoria, tags=["Categorias"])
def create_categoria(categoria: categoria_model.CategoriaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea una nueva categoria.
    """
    db_categoria = categoria_model.CategoriaDB(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.get("/categorias", response_model=List[categoria_model.Categoria], tags=["Categorias"])
def get_categorias(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las categorias.
    """
    categorias = db.query(categoria_model.CategoriaDB).all()
    return categorias

@router.get("/categorias/{id_categoria}", response_model=categoria_model.Categoria, tags=["Categorias"])
def get_categoria(id_categoria: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoria específica por su ID.
    """
    categoria = db.query(categoria_model.CategoriaDB).filter(categoria_model.CategoriaDB.ID_CATEGORIA == id_categoria).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return categoria

@router.put("/categorias/{id_categoria}", response_model=categoria_model.Categoria, tags=["Categorias"])
def update_categoria(id_categoria: int, categoria: categoria_model.CategoriaCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza una categoria existente.
    """
    db_categoria = db.query(categoria_model.CategoriaDB).filter(categoria_model.CategoriaDB.ID_CATEGORIA == id_categoria).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    update_data = categoria.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_categoria, key, value)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.delete("/categorias/{id_categoria}", status_code=204, tags=["Categorias"])
def delete_categoria(id_categoria: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina una categoria existente.
    """
    db_categoria = db.query(categoria_model.CategoriaDB).filter(categoria_model.CategoriaDB.ID_CATEGORIA == id_categoria).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    db.delete(db_categoria)
    db.commit()
    return
