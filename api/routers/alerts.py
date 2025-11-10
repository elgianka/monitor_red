from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import alert as alert_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/alerts", response_model=alert_model.Alert, tags=["Alerts"])
def create_alert(alert: alert_model.AlertCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Crea una nueva alerta.
    """
    db_alert = alert_model.AlertDB(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/alerts", response_model=List[alert_model.Alert], tags=["Alerts"])
def get_alerts(db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Obtiene una lista de todas las alertas.
    """
    alerts = db.query(alert_model.AlertDB).all()
    return alerts

@router.get("/alerts/active", response_model=List[alert_model.Alert], tags=["Alerts"])
def get_active_alerts(db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Obtiene una lista de todas las alertas activas.
    """
    alerts = db.query(alert_model.AlertDB).filter(alert_model.AlertDB.estado_alerta == 'ACTIVA').all()
    return alerts

@router.get("/alerts/{id_alerta}", response_model=alert_model.Alert, tags=["Alerts"])
def get_alert(id_alerta: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Obtiene una alerta específica por su ID.
    """
    alert = db.query(alert_model.AlertDB).filter(alert_model.AlertDB.id_alerta == id_alerta).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/alerts/{id_alerta}", response_model=alert_model.Alert, tags=["Alerts"])
def update_alert(id_alerta: int, alert: alert_model.AlertUpdate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Actualiza una alerta existente.
    """
    db_alert = db.query(alert_model.AlertDB).filter(alert_model.AlertDB.id_alerta == id_alerta).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    update_data = alert.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_alert, key, value)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.delete("/alerts/{id_alerta}", status_code=204, tags=["Alerts"])
def delete_alert(id_alerta: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    """
    Elimina una alerta existente.
    """
    db_alert = db.query(alert_model.AlertDB).filter(alert_model.AlertDB.id_alerta == id_alerta).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return
