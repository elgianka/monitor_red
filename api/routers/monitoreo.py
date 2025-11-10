from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
from pydantic import BaseModel

from ..models import monitoreo as monitoreo_model, user as user_model, host as host_model, estado as estado_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

# Pydantic model for the POST request body
class MonitoreoPostBody(BaseModel):
    ping_result: Optional[float] = None

@router.post("/monitoreo/{host_id}", response_model=monitoreo_model.Monitoreo, tags=["Monitoreo"])
def create_monitoreo_entry(
    host_id: int,
    monitoreo: MonitoreoPostBody,
    db: Session = Depends(get_db),
    current_user: user_model.UserDB = Depends(get_current_user)
):
    """
    Crea una nueva entrada de monitoreo para un host y actualiza el estado del host.
    """
    db_host = db.query(host_model.HostDB).filter(host_model.HostDB.ID_HOST == host_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Host not found")

    # Get status IDs
    estado_activo = db.query(estado_model.EstadoDB).filter(estado_model.EstadoDB.NOM_ESTADO == "Activo").first()
    estado_inactivo = db.query(estado_model.EstadoDB).filter(estado_model.EstadoDB.NOM_ESTADO == "Inactivo").first()

    if not estado_activo or not estado_inactivo:
        raise HTTPException(status_code=500, detail="Estados 'Activo' o 'Inactivo' no encontrados en la base de datos.")

    if monitoreo.ping_result is not None and monitoreo.ping_result >= 0:
        db_host.ID_ESTADO = estado_activo.ID_ESTADO
    else:
        db_host.ID_ESTADO = estado_inactivo.ID_ESTADO

    db.add(db_host) # Add the modified host object to the session
    db.commit()    # Commit the changes to the host
    db.refresh(db_host) # Refresh the host object to reflect changes

    new_monitoreo_entry = monitoreo_model.MonitoreoDB(
        ID_HOST=host_id,
        PING_RESULT=monitoreo.ping_result,
        TIMESTAMP=datetime.datetime.utcnow()
    )
    db.add(new_monitoreo_entry)
    db.commit()
    db.refresh(new_monitoreo_entry)
    return new_monitoreo_entry

@router.get("/monitoreo/{host_id}", response_model=List[monitoreo_model.Monitoreo], tags=["Monitoreo"])
def get_monitoreo_by_host(
    host_id: int,
    start_date: Optional[datetime.datetime] = Query(None, description="Fecha de inicio para filtrar el monitoreo"),
    end_date: Optional[datetime.datetime] = Query(None, description="Fecha de fin para filtrar el monitoreo"),
    db: Session = Depends(get_db),
    current_user: user_model.UserDB = Depends(get_current_user)
):
    """
    Obtiene los datos de monitoreo (ping) para un host específico, con filtrado opcional por rango de fechas.
    """
    query = db.query(monitoreo_model.MonitoreoDB).filter(monitoreo_model.MonitoreoDB.ID_HOST == host_id)

    if start_date:
        query = query.filter(monitoreo_model.MonitoreoDB.TIMESTAMP >= start_date)
    if end_date:
        query = query.filter(monitoreo_model.MonitoreoDB.TIMESTAMP <= end_date)

    monitoreos = query.all()

    if not monitoreos:
        raise HTTPException(status_code=404, detail="No se encontraron datos de monitoreo para este host en el rango de fechas especificado.")
    return monitoreos
