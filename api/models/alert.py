from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class AlertBase(BaseModel):
    id_host: int
    tipo_alerta: str
    estado_alerta: str
    timestamp_inicio: str
    timestamp_fin: str | None = None
    id_monitoreo_inicio: int | None = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(AlertBase):
    id_host: Optional[int] = None
    tipo_alerta: Optional[str] = None
    estado_alerta: Optional[str] = None
    timestamp_inicio: Optional[str] = None

class Alert(AlertBase):
    id_alerta: int

    class Config:
        orm_mode = True

class AlertDB(Base):
    __tablename__ = "TB_ALERTA"

    id_alerta = Column("ID_ALERTA", Integer, primary_key=True, index=True)
    id_host = Column("ID_HOST", Integer, ForeignKey("TB_HOST.ID_HOST"))
    tipo_alerta = Column("TIPO_ALERTA", String)
    estado_alerta = Column("ESTADO_ALERTA", String)
    timestamp_inicio = Column("TIMESTAMP_INICIO", DateTime)
    timestamp_fin = Column("TIMESTAMP_FIN", DateTime, nullable=True)
    id_monitoreo_inicio = Column("ID_MONITOREO_INICIO", Integer)

    host = relationship("HostDB")
