from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.session import Base

class EstadoBase(BaseModel):
    NOM_ESTADO: str

class EstadoCreate(EstadoBase):
    pass

class Estado(EstadoBase):
    ID_ESTADO: int

    class Config:
        from_attributes = True

class EstadoDB(Base):
    __tablename__ = "TB_ESTADO"

    ID_ESTADO = Column(Integer, primary_key=True, index=True)
    NOM_ESTADO = Column(String, nullable=False, unique=True)

    hosts = relationship("HostDB", back_populates="estado")
