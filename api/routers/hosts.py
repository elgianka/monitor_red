from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..models import host as host_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/hosts", response_model=host_model.Host, tags=["Hosts"])
def create_host(host: host_model.HostCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea un nuevo host.
    MODIFICADO: Acepta datos incompletos y rellena con valores por defecto para compatibilidad.
    """
    host_data = host.dict()
    
    # Rellenar campos faltantes con valores por defecto (ID=1)
    default_fields = {
        "ID_MODELO": 1,
        "ID_RESPONSABLE": 1,
        "ID_UBICACION": 1,
        "ID_PROCESO": 1,
        "ID_CATEGORIA": 1,
        "ID_ESTADO": 1,
        "ID_SEDE": 1
    }

    for field, default_value in default_fields.items():
        if field not in host_data or host_data[field] is None:
            host_data[field] = default_value

    db_host = host_model.HostDB(**host_data)
    db.add(db_host)
    db.commit()
    db.refresh(db_host)

    # Volver a cargar el host con la relación 'estado' para la respuesta
    created_host_with_relations = db.query(host_model.HostDB).options(joinedload(host_model.HostDB.estado)).filter(host_model.HostDB.ID_HOST == db_host.ID_HOST).first()
    
    return created_host_with_relations

@router.get("/hosts", response_model=List[host_model.Host], tags=["Hosts"])
def get_hosts(db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Obtiene una lista de todos los hosts.
    """
    hosts = db.query(host_model.HostDB).options(joinedload(host_model.HostDB.estado)).all()
    return hosts

@router.get("/hosts/{id_host}", response_model=host_model.Host, tags=["Hosts"])
def get_host(id_host: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
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
