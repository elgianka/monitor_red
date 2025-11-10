from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.session import Base

class GerenciaBase(BaseModel):
    NOM_GERENCIA: str

class GerenciaCreate(GerenciaBase):
    pass

class Gerencia(GerenciaBase):
    ID_GERENCIA: int

    class Config:
        from_attributes = True

class GerenciaDB(Base):
    __tablename__ = "TB_GERENCIA"

    ID_GERENCIA = Column(Integer, primary_key=True, index=True)
    NOM_GERENCIA = Column(String, nullable=False, unique=True)

    areas = relationship("AreaDB", back_populates="gerencia")
