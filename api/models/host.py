from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
import datetime
# CORRECCIÓN CLAVE: Importar la Base compartida
from ..db.session import Base

# SQLAlchemy Model
class HostDB(Base):
    __tablename__ = "TB_HOST"

    # Claves Primarias y Campos Propios
    ID_HOST = Column(Integer, primary_key=True, index=True)
    NOM_HOST = Column(String, nullable=False)
    IP_HOST = Column(String, nullable=False, unique=True)
    MAC_HOST = Column(String)
    NUM_SERIE = Column(String)
    FIRMWARE_VERSION = Column(String)
    FECHA_ALTA = Column(Date)
    ANHO_ALTA = Column(Integer)
    LIM_SUP_PING = Column(Float)
    LIM_INF_PING = Column(Float)

    # Claves Foráneas (Se asume que hay una tabla de modelos por cada uno de estos)
    ID_MODELO = Column(Integer, ForeignKey("TB_MODELO.ID_MODELO"))
    ID_RESPONSABLE = Column(Integer, ForeignKey("TB_RESPONSABLE.ID_RESPONSABLE"))
    ID_UBICACION = Column(Integer, ForeignKey("TB_UBICACION.ID_UBICACION"))
    ID_SEDE = Column(Integer, ForeignKey("TB_SEDE.ID_SEDE"))
    ID_PROCESO = Column(Integer, ForeignKey("TB_PROCESO.ID_PROCESO"))
    ID_CATEGORIA = Column(Integer, ForeignKey("TB_CATEGORIA.ID_CATEGORIA"))
    ID_ESTADO = Column(Integer, ForeignKey("TB_ESTADO.ID_ESTADO"))

    # Relaciones (Usando cadenas para evitar dependencias circulares)
    modelo = relationship("ModeloDB", back_populates="hosts")
    responsable = relationship("ResponsableDB", back_populates="hosts")
    ubicacion = relationship("UbicacionDB", back_populates="hosts")
    proceso = relationship("ProcesoDB", back_populates="hosts")
    categoria = relationship("CategoriaDB", back_populates="hosts")
    estado = relationship("EstadoDB", back_populates="hosts")
    sede = relationship("SedeDB", back_populates="hosts")

    # Relación a alertas (bidireccional)
    alerts = relationship("AlertDB", back_populates="host", cascade="all, delete-orphan")
    monitoreos = relationship("MonitoreoDB", back_populates="host", cascade="all, delete-orphan")


from .estado import Estado
from .ubicacion import Ubicacion

# Pydantic Model for API responses
class Host(BaseModel):
    ID_HOST: int
    NOM_HOST: str
    IP_HOST: str
    MAC_HOST: Optional[str] = None
    NUM_SERIE: Optional[str] = None
    FIRMWARE_VERSION: Optional[str] = None
    FECHA_ALTA: Optional[datetime.date] = None
    ANHO_ALTA: Optional[int] = None
    ID_MODELO: int # Se mantendrán como ID por ahora para no sobrecargar la respuesta
    ID_RESPONSABLE: int
    ID_PROCESO: int
    ID_CATEGORIA: int
    estado: Optional[Estado] = None # <-- CAMBIO CLAVE: El estado ahora es opcional
    ubicacion: Optional[Ubicacion] = None # <-- CAMBIO CLAVE: Se añade la ubicación completa
    LIM_SUP_PING: Optional[float] = None
    LIM_INF_PING: Optional[float] = None

    class Config:
        from_attributes = True

class HostCreate(BaseModel):
    NOM_HOST: str
    IP_HOST: str
    MAC_HOST: Optional[str] = None
    NUM_SERIE: Optional[str] = None
    FIRMWARE_VERSION: Optional[str] = None
    FECHA_ALTA: Optional[datetime.date] = None
    ANHO_ALTA: Optional[int] = None
    ID_MODELO: Optional[int] = None
    ID_RESPONSABLE: Optional[int] = None
    ID_UBICACION: Optional[int] = None
    ID_PROCESO: Optional[int] = None
    ID_CATEGORIA: Optional[int] = None
    ID_ESTADO: Optional[int] = None
    LIM_SUP_PING: Optional[float] = None
    LIM_INF_PING: Optional[float] = None

class HostUpdate(BaseModel):
    NOM_HOST: Optional[str] = None
    IP_HOST: Optional[str] = None
    MAC_HOST: Optional[str] = None
    NUM_SERIE: Optional[str] = None
    FIRMWARE_VERSION: Optional[str] = None
    FECHA_ALTA: Optional[datetime.date] = None
    ANHO_ALTA: Optional[int] = None
    ID_MODELO: Optional[int] = None
    ID_RESPONSABLE: Optional[int] = None
    ID_UBICACION: Optional[int] = None
    ID_PROCESO: Optional[int] = None
    ID_CATEGORIA: Optional[int] = None
    ID_ESTADO: Optional[int] = None
    LIM_SUP_PING: Optional[float] = None
    LIM_INF_PING: Optional[float] = None