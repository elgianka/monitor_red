from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..db.session import Base

class ProcesoBase(BaseModel):
    NOM_PROCESO: str
    DET_PROCESO: str | None = None

class ProcesoCreate(ProcesoBase):
    pass

class Proceso(ProcesoBase):
    ID_PROCESO: int

    class Config:
        from_attributes = True

class ProcesoDB(Base):
    __tablename__ = "TB_PROCESO"

    ID_PROCESO = Column(Integer, primary_key=True, index=True)
    NOM_PROCESO = Column(String, nullable=False)
    DET_PROCESO = Column(Text)

    hosts = relationship("HostDB", back_populates="proceso")
