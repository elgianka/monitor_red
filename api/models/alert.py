from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base
# Se elimina la importación directa de HostDB para evitar la circularidad

class AlertBase(BaseModel):
    id_host: int
    tipo_alerta: str
    estado_alerta: str
    # Se recomienda usar datetime.datetime en Pydantic, pero mantenemos 'str' si es consistente con otros modelos.
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
    timestamp_fin: Optional[str] = None # Permitir actualizar el fin

class Alert(AlertBase):
    id_alerta: int

    class Config:
        # Pydantic V2 utiliza from_attributes
        from_attributes = True

class AlertDB(Base):
    __tablename__ = "TB_ALERTA"

    id_alerta = Column("ID_ALERTA", Integer, primary_key=True, index=True)
    # Definición de la clave foránea
    id_host = Column("ID_HOST", Integer, ForeignKey("TB_HOST.ID_HOST"))
    tipo_alerta = Column("TIPO_ALERTA", String)
    estado_alerta = Column("ESTADO_ALERTA", String)
    timestamp_inicio = Column("TIMESTAMP_INICIO", DateTime)
    timestamp_fin = Column("TIMESTAMP_FIN", DateTime, nullable=True)
    id_monitoreo_inicio = Column("ID_MONITOREO_INICIO", Integer, nullable=True) # Se añade nullable=True si es opcional

    # CORRECCIÓN CLAVE: Usar la cadena de texto "HostDB" para la relación
    # El back_populates debe coincidir con el nombre de la relación definida en HostDB ("alerts")
    host = relationship("HostDB", back_populates="alerts")
