from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional
import datetime

Base = declarative_base()

# SQLAlchemy Model
class HostDB(Base):
    __tablename__ = "TB_HOST"

    ID_HOST = Column(Integer, primary_key=True, index=True)
    NOM_HOST = Column(String, nullable=False)
    IP_HOST = Column(String, nullable=False, unique=True)
    MAC_HOST = Column(String)
    NUM_SERIE = Column(String)
    FIRMWARE_VERSION = Column(String)
    FECHA_ALTA = Column(Date)
    AÑO_ALTA = Column(Integer)
    ID_MODELO = Column(Integer)
    ID_RESPONSABLE = Column(Integer)
    ID_UBICACION = Column(Integer)
    ID_PROCESO = Column(Integer)
    ID_CATEGORIA = Column(Integer)
    ID_ESTADO = Column(Integer)
    LIM_SUP_PING = Column(Float)
    LIM_INF_PING = Column(Float)

# Pydantic Model for API responses
class Host(BaseModel):
    ID_HOST: int
    NOM_HOST: str
    IP_HOST: str
    MAC_HOST: Optional[str] = None
    NUM_SERIE: Optional[str] = None
    FIRMWARE_VERSION: Optional[str] = None
    FECHA_ALTA: Optional[datetime.date] = None
    AÑO_ALTA: Optional[int] = None
    ID_MODELO: int
    ID_RESPONSABLE: int
    ID_UBICACION: int
    ID_PROCESO: int
    ID_CATEGORIA: int
    ID_ESTADO: int
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
    AÑO_ALTA: Optional[int] = None
    ID_MODELO: int
    ID_RESPONSABLE: int
    ID_UBICACION: int
    ID_PROCESO: int
    ID_CATEGORIA: int
    ID_ESTADO: int
    LIM_SUP_PING: Optional[float] = None
    LIM_INF_PING: Optional[float] = None

class HostUpdate(BaseModel):
    NOM_HOST: Optional[str] = None
    IP_HOST: Optional[str] = None
    MAC_HOST: Optional[str] = None
    NUM_SERIE: Optional[str] = None
    FIRMWARE_VERSION: Optional[str] = None
    FECHA_ALTA: Optional[datetime.date] = None
    AÑO_ALTA: Optional[int] = None
    ID_MODELO: Optional[int] = None
    ID_RESPONSABLE: Optional[int] = None
    ID_UBICACION: Optional[int] = None
    ID_PROCESO: Optional[int] = None
    ID_CATEGORIA: Optional[int] = None
    ID_ESTADO: Optional[int] = None
    LIM_SUP_PING: Optional[float] = None
    LIM_INF_PING: Optional[float] = None
