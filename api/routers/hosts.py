from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import host as host_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/hosts", response_model=host_model.Host, tags=["Hosts"])
def create_host(host: host_model.HostCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea un nuevo host.
    """
    db_host = host_model.HostDB(**host.dict())
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

@router.get("/hosts", response_model=List[host_model.Host], tags=["Hosts"])
def get_hosts(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los hosts.
    """
    hosts = db.query(host_model.HostDB).all()
    return hosts

@router.get("/hosts/{id_host}", response_model=host_model.Host, tags=["Hosts"])
def get_host(id_host: int, db: Session = Depends(get_db)):
    """
    Obtiene un host específico por su ID.
    """
    host = db.query(host_model.HostDB).filter(host_model.HostDB.ID_HOST == id_host).first()
    if host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    return host

@router.put("/hosts/{id_host}", response_model=host_model.Host, tags=["Hosts"])
def update_host(id_host: int, host: host_model.HostUpdate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza un host existente.
    """
    db_host = db.query(host_model.HostDB).filter(host_model.HostDB.ID_HOST == id_host).first()
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    update_data = host.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_host, key, value)
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

@router.delete("/hosts/{id_host}", status_code=204, tags=["Hosts"])
def delete_host(id_host: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina un host existente.
    """
    db_host = db.query(host_model.HostDB).filter(host_model.HostDB.ID_HOST == id_host).first()
    if db_host is None:
        raise HTTPException(status_code=404, detail="Host not found")
    db.delete(db_host)
    db.commit()
    return
