from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.session import Base

class UbicacionBase(BaseModel):
    NOM_UBICACION: str

class UbicacionCreate(UbicacionBase):
    pass

class Ubicacion(UbicacionBase):
    ID_UBICACION: int

    class Config:
        from_attributes = True

class UbicacionDB(Base):
    __tablename__ = "TB_UBICACION"

    ID_UBICACION = Column(Integer, primary_key=True, index=True)
    NOM_UBICACION = Column(String, nullable=False, unique=True)

    hosts = relationship("HostDB", back_populates="ubicacion")
